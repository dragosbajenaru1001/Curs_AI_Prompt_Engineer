# LangGraph Handoff Demo

A multi-agent customer support system built with **LangGraph**, demonstrating the **handoff pattern** using `llama-3.1-8b-instant` via the Groq API.

Execution flow: `START → triage → [billing | technical] → END`

---

## How This Notebook Was Built — Prompt Chaining

> **Prompt chaining** is a technique where the output of one prompt becomes the input (or context) for the next. Each prompt in the chain has a focused, narrow responsibility; together they compose a complex behavior that no single prompt could reliably produce alone.

The notebook was created through the following chain of prompts, each building on what the previous step established.

---

### Step 1 — Define the Problem Space

**Prompt:**
> "Design a customer support system with multiple specialized agents. The system should receive a customer request, classify it, and route it to the appropriate specialist — either billing or technical support — without a central coordinator."

**What this produced:**
- The overall architecture: `triage → specialist → END`
- The insight that `Command(goto=...)` in LangGraph enables direct agent-to-agent handoffs
- The three-agent structure: `triage`, `billing`, `technical`

---

### Step 2 — Model the State

**Prompt:**
> "Define the shared state that all agents will read and write. It must track: the conversation history, which agent is currently active, and the reason for any handoff."

**What this produced:**
```python
class GraphState(TypedDict):
    messages:       List[BaseMessage]
    current_agent:  str
    handoff_reason: str
```

The state is the contract between agents. Every `Command` update writes back into this structure, giving each downstream agent full context.

---

### Step 3 — Define Structured Outputs

**Prompt:**
> "The LLM must return structured decisions, not free text. Define Pydantic schemas so the triage agent returns a routing decision, and specialist agents return both a response and an optional handoff instruction."

**What this produced:**
```python
class TriageDecision(BaseModel):
    next_agent: Literal["billing", "technical"]
    reason: str

class HandoffDecision(BaseModel):
    needs_handoff: bool
    handoff_to: Optional[Literal["technical"]] = None
    response: str
```

Using `llm.with_structured_output(Schema)` forces the model to return machine-readable decisions rather than prose, making routing logic deterministic and safe.

---

### Step 4 — Write the Triage Prompt

**Prompt:**
> "Write a concise system prompt for the triage agent. It must classify the incoming customer message into exactly one of two categories — billing or technical — with no ambiguity. Keep it under 5 lines."

**What this produced:**
```python
TRIAGE_PROMPT = (
    "Triage suport clienți. Clasifică cererea în maxim un cuvânt:\n"
    "  billing → facturi, plăți\n"
    "  technical → erori, conexiune, configurare\n"
    "Alege un singur agent."
)
```

Short, imperative, exhaustive in scope. The two-word examples (`facturi, plăți` / `erori, conexiune`) anchor the model's classification without over-constraining it.

---

### Step 5 — Write the Billing Agent Prompt

**Prompt:**
> "Write a system prompt for the billing specialist. It should answer questions about invoices and payments in at most 2 sentences. If the problem turns out to be technical, it must signal a handoff to the technical agent."

**What this produced (inline in `billing_node`):**
```python
system = (
    "Agent billing. Răspunde scurt la întrebări despre facturi și plăți. "
    "Dacă problema e tehnică: needs_handoff=true, handoff_to='technical'. "
    "Răspuns maxim 2 propoziții."
)
```

The explicit instruction `needs_handoff=true, handoff_to='technical'` mirrors the Pydantic field names, teaching the model exactly how to signal a cross-agent transfer via structured output.

---

### Step 6 — Write the Technical Agent Prompt

**Prompt:**
> "Write a system prompt for the technical specialist. It should resolve technical problems concisely. It must never initiate a further handoff. If it received a handoff from billing, inject the reason as additional context."

**What this produced (inline in `technical_node`):**
```python
context = f"\nContext: {state['handoff_reason']}" if state["handoff_reason"] else ""
system = (
    f"Agent technical. Rezolvă probleme tehnice scurt și clar.{context} "
    "needs_handoff=false. Răspuns maxim 2 propoziții."
)
```

The injected `context` variable closes the chain: the `handoff_reason` written by the billing agent in Step 5 becomes the grounding context for the technical agent here. This is prompt chaining at the runtime level — output of one node feeds the prompt of the next.

---

### Step 7 — Assemble the Graph

**Prompt:**
> "Wire the nodes into a LangGraph `StateGraph`. The only fixed edge is `START → triage`. All other transitions are driven by `Command(goto=...)` returned by each node."

**What this produced:**
```python
builder = StateGraph(GraphState)
builder.add_node("triage",    triage_node)
builder.add_node("billing",   billing_node)
builder.add_node("technical", technical_node)
builder.add_edge(START, "triage")
graph = builder.compile()
```

There are no conditional edges or routing functions — the graph is intentionally minimal. Control flow lives entirely inside the agent nodes.

---

## Prompt Chain Summary

| Step | Prompt Focus | Output |
|------|-------------|--------|
| 1 | Problem space & architecture | 3-agent handoff design |
| 2 | Shared state schema | `GraphState` TypedDict |
| 3 | Structured LLM outputs | `TriageDecision`, `HandoffDecision` |
| 4 | Triage classification prompt | `TRIAGE_PROMPT` constant |
| 5 | Billing specialist prompt | Inline system prompt + handoff signal |
| 6 | Technical specialist prompt | Inline system prompt + injected context |
| 7 | Graph assembly | `StateGraph` with `Command`-driven routing |

Each step produces a concrete artifact that the next step depends on. No step could be reordered without breaking the chain.

---

## Setup

```bash
pip install langgraph langchain-groq
```

Set your Groq API key (in Google Colab via `userdata`, or as an environment variable):

```python
import os
os.environ["GROQ_API_KEY"] = "your-key-here"
```

Get a free API key at [console.groq.com/keys](https://console.groq.com/keys).

---

## Running

Open [Langgraph_handoff_demo.ipynb](Langgraph_handoff_demo.ipynb) and run all cells. The default test message is:

> *"Am o taxă necunoscută pe factură din această lună."*
> ("I have an unknown charge on my invoice this month.")

Expected output traces through `[TRIAGE] → billing` and prints the billing agent's response.
