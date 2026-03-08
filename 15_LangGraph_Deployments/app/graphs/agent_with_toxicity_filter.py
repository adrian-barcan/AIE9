"""An agent graph with a post-response toxicity check loop.

After the agent responds, a secondary node evaluates the response for toxicity or profanity.
If safe, end; otherwise, loop back to the agent with instructions to rewrite the response politely.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, SystemMessage

from app.state import MessagesState
from app.models import get_chat_model
from app.tools import get_tool_belt


class ToxicityResult(BaseModel):
    is_toxic: bool = Field(description="Whether the response contains any toxicity, profanity, or inappropriate content")


def _build_model_with_tools():
    """Return a chat model instance bound to the current tool belt."""
    model = get_chat_model()
    return model.bind_tools(get_tool_belt())


def call_model(state: MessagesState) -> dict:
    """Invoke the model with the accumulated messages and append its response."""
    model = _build_model_with_tools()
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


def route_to_action_or_toxicity_check(state: MessagesState):
    """Decide whether to execute tools or run the toxicity evaluator."""
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "action"
    return "toxicity_check"


_toxicity_prompt = ChatPromptTemplate.from_template(
    "Evaluate the following response for toxicity, profanity, anger, or generally inappropriate content. "
    "If the response is completely safe, polite, and professional, mark it as NOT toxic.\n\n"
    "Response to Evaluate:\n{final_response}"
)


def toxicity_node(state: MessagesState) -> dict:
    """Evaluate toxicity of the latest response."""
    if len(state["messages"]) > 10:
        return {"messages": [AIMessage(content="TOXICITY:END")]}

    final_response = state["messages"][-1]

    structured_model = get_chat_model(model_name="gpt-4o-mini").with_structured_output(ToxicityResult)
    result = (_toxicity_prompt | structured_model).invoke(
        {
            "final_response": final_response.content,
        }
    )

    decision = "Y" if result.is_toxic else "N"
    if result.is_toxic:
        return {"messages": [SystemMessage(content="TOXICITY DETECTED: Your previous response was flagged as inappropriate or toxic. Please rewrite your response to be polite, professional, and safe. Do not use any profanity.")]}

    return {"messages": [AIMessage(content=f"TOXICITY:{decision}")]}


def toxicity_decision(state: MessagesState):
    """Terminate on 'TOXICITY:N' or loop otherwise; guard against infinite loops."""
    if any(getattr(m, "content", "") == "TOXICITY:END" for m in state["messages"][-1:]):
        return END

    last = state["messages"][-1]
    text = getattr(last, "content", "")
    if "TOXICITY:N" in text:
        return "end"
    return "continue"


def build_graph():
    """Build an agent graph with an auxiliary toxicity evaluation subgraph."""
    graph = StateGraph(MessagesState)
    tool_node = ToolNode(get_tool_belt())
    graph.add_node("agent", call_model)
    graph.add_node("action", tool_node)
    graph.add_node("toxicity_check", toxicity_node)
    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        route_to_action_or_toxicity_check,
        {"action": "action", "toxicity_check": "toxicity_check"},
    )
    graph.add_conditional_edges(
        "toxicity_check",
        toxicity_decision,
        {"continue": "agent", "end": END, END: END},
    )
    graph.add_edge("action", "agent")
    return graph


graph = build_graph().compile()
