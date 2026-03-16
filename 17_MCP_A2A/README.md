<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

## <h1 align="center" id="heading">Session 17: Model Context Protocol (MCP) & Agent-to-Agent (A2A) Protocol</h1>

| Session Sheet | Recording     | Slides        | Repo         | Homework      | Feedback       |
|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|
| [MCP Servers & A2A](../00_Docs/Session_Sheets/17_MCP_Servers_and_A2A) |[Recording!](https://us02web.zoom.us/rec/share/_iJT-kZiYacyz23fjU3N7w7mZIUFJqGXV48RDqCkCY3avsmngKtzK0SNs0I7k74.xICq6NSv6l6GqAFU) <br> passcode: `fJ9tx4h.`| [Session 17 Slides](https://www.canva.com/design/DAG-ELapG4g/6vDMm63RBwKVsSZvheorVA/edit?utm_content=DAG-ELapG4g&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) | You are here! | [(Optional) Session 17 Assignment: MCP Servers & A2A](https://forms.gle/qtjQFfoEF8aykTWy5) | [Feedback 3/12](https://forms.gle/sJwD1a6LLn9NU9s48) |
---

## 📚 Useful Resources

**MCP (Model Context Protocol)**
- [MCP Official Docs](https://modelcontextprotocol.io/) — Spec, tutorials, and guides
- [MCP-UI](https://mcpui.dev/) — Official standard for interactive UI in MCP
- [MCP Auth Guide (Auth0)](https://auth0.com/blog/mcp-specs-update-all-about-auth/) — Deep dive into MCP auth spec updates

**A2A (Agent-to-Agent Protocol)**
- [A2A Official Docs](https://a2a-protocol.org/latest/) — Spec and guides
- [A2A GitHub Repo](https://github.com/a2aproject/A2A) — Protocol spec and implementations
- [Announcing A2A (Google Blog)](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) — Protocol vision and motivation

**MCP vs A2A**
- [A2A and MCP (Official)](https://a2a-protocol.org/latest/topics/a2a-and-mcp/) — How they complement each other

---

# Running the MCP Server

### 1. Install dependencies

```bash
uv sync
```

### 2. Set up environment variables

Copy the example env file and fill in your OpenAI API key:

```bash
cp .env.example .env
```

### 3. Run the MCP server locally

```bash
uv run server.py
```

The server will start on `http://localhost:8000`.

### 4. Expose the server with ngrok (for remote/Claude Desktop access)

In a separate terminal, start an ngrok tunnel:

```bash
ngrok http 8000
```

Copy the ngrok forwarding URL (e.g. `https://xxxx-xx-xx-xx-xx.ngrok-free.app`) and restart the server with it:

```bash
ISSUER_URL=https://xxxx-xx-xx-xx-xx.ngrok-free.app uv run server.py
```

> **Note:** The `ISSUER_URL` must match the public URL clients use to reach the server, otherwise OAuth authentication will fail.

---

# Build 🏗️

In today's assignment, we'll be building an MCP server with OAuth authentication — a cat shop application that exposes tools for browsing products, managing a cart, and checking out.

- 🤝 Breakout Room #1
  - Set up the MCP server with OAuth and the product database
  - Explore the MCP tools: `list_products`, `get_product`, `add_to_cart`, `view_cart`, `remove_from_cart`, `checkout`

- 🤝 Breakout Room #2
  - Connect an MCP client to the server
  - Build an end-to-end interaction flow using the MCP tools

# Ship 🚢

The completed MCP server and client integration!

### Deliverables

- A short Loom of either:
  - the MCP server you built and a demo of the client interacting with it; or
  - the notebook you created for the Advanced Build

# Share 🚀

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped an MCP server with OAuth authentication! 🎉🤖

🔍 Three Key Takeaways:
1️⃣
2️⃣
3️⃣

Let's continue pushing the boundaries of what's possible in the world of AI and tool integration. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#MCP #ModelContextProtocol #OAuth #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```

# Submitting Your Homework [OPTIONAL]

## Main Homework Assignment

Follow these steps to prepare and submit your homework assignment:

1. Review the MCP server code in `server.py` and the `app/` directory
2. Run the MCP server locally using `uv run server.py`
3. Connect to the server using an MCP client (e.g., Claude Desktop, or a custom client)
4. Test all available tools: browsing products, adding to cart, viewing cart, removing items, and checkout
5. Record a Loom video reviewing what you have learned from this session

## Questions

### ❓ Question #1:

Why is OAuth important for MCP servers, and what security considerations should you keep in mind when exposing tools to AI clients?

#### ✅ Answer:

OAuth is important for MCP servers because these servers expose powerful tools (like browsing products, managing carts, making purchases) that AI clients can call autonomously. Without proper authentication, anyone could access those tools and perform actions on behalf of users without their consent.

OAuth solves this by ensuring that:
1. **Only authorized clients** can connect to the server (the client must go through the OAuth flow to get a valid token).
2. **Users explicitly grant permission** for what the AI client can do, so the agent can't just do whatever it wants.
3. **Tokens are scoped and temporary**, limiting the blast radius if something goes wrong.

Key security considerations:
- **Always validate tokens server-side** - never trust the client blindly.
- **Use HTTPS in production** so tokens aren't leaked in transit.
- **Keep scopes narrow** - only grant the AI client the minimum permissions it actually needs (principle of least privilege).
- **Handle token expiration and revocation** - tokens should expire, and you should be able to revoke them if a client is compromised.
- **Be careful with sensitive operations** - tools that modify data or trigger purchases should have extra checks, because an AI agent might call them in ways a human wouldn't expect.

### ❓ Question #2:

What is the Agent-to-Agent (A2A) protocol, and how does it differ from MCP in terms of purpose and architecture? When would you choose A2A over MCP?

#### ✅ Answer:

The **Agent-to-Agent (A2A) protocol** is an open standard (introduced by Google) that enables AI agents to communicate, discover each other's capabilities, and collaborate on tasks even if they're built with different frameworks or run on different platforms.

**How it differs from MCP:**
- **MCP** is about connecting an AI agent to **tools and data sources**. It standardizes how a single agent accesses external capabilities (APIs, databases, services). Think of it as giving an agent its "hands" to interact with the world.
- **A2A** is about connecting **agents to other agents**. It standardizes how multiple agents discover each other, delegate tasks, and exchange results. Think of it as giving agents the ability to "talk to each other" and work as a team.

In terms of architecture, MCP follows a **client-server model** (one agent calls tools on a server), while A2A is more **peer-to-peer**, agents publish "Agent Cards" describing what they can do, and other agents can discover and delegate tasks to them.

**When to choose A2A over MCP:**
- Use **MCP** when you need a single agent to access tools, APIs, or data sources.
- Use **A2A** when you need multiple specialized agents to collaborate — for example, a "research agent" delegating a coding task to a "developer agent," or an orchestrator coordinating several domain-specific agents.

They're actually complementary: an agent might use MCP to access its tools internally, while using A2A to communicate with other agents externally.

## Activity 1: Extend the MCP Server

Add at least one new tool to the cat shop MCP server (e.g., `search_products`, `update_cart_quantity`, or `get_order_history`). Ensure the new tool integrates properly with the existing database and OAuth authentication. Demo the new tool through an MCP client and include it in your Loom video.

**Implemented tools:**
- `search_products`: Takes a `query` string and performs a case-insensitive search across product names and descriptions using SQL `LIKE`. Returns all matching products with their full details (id, name, description, price, category).
- `update_cart_quantity`: Takes a `product_name` (partial match) and a `quantity` to update an item in the cart. Handles ambiguous matches, negative quantities, and setting quantity to 0 removes the item.

## Advanced Activity: Build a Custom MCP Client

Build a custom MCP client that connects to the cat shop server over Streamable HTTP, authenticates via OAuth, and orchestrates a multi-step shopping flow (browse → add to cart → checkout). Compare the developer experience of MCP-based tool integration vs. traditional REST API calls.

Include your findings and a demo in your Loom video.
