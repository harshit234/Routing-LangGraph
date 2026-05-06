"""
Parishiksha Retrieval Assistant
LangGraph-based multi-agent chatbot: Router → Retrieve / Direct Answer → Generate
"""

import os, json, re
from flask import Flask, render_template, request, Response, jsonify
from typing import TypedDict, List
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from knowledge_base import (
    COURSE_NOTES, get_notes_for_week, get_all_notes, get_available_weeks,
)
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
)


# ──────────────────── State ────────────────────
class QueryState(TypedDict):
    query: str
    route: str
    week: str
    reason: str
    context: str
    response: str
    trace: List[dict]


# ──────────────────── Nodes ────────────────────

def router_node(state: QueryState) -> dict:
    """Classify the query: retrieve course notes or answer directly."""
    system = (
        "You are a routing agent for 'Parishiksha', a university AI/ML course assistant.\n"
        "The course has 10 weeks:\n"
        "  Week 1: Intro to AI & Random Prediction\n"
        "  Week 2: Linear Models & Regression\n"
        "  Week 3: Neural Networks Fundamentals\n"
        "  Week 4: CNNs\n"
        "  Week 5: RNNs\n"
        "  Week 6: Word Embeddings & NLP\n"
        "  Week 7: Seq2Seq Models\n"
        "  Week 8: Attention Mechanisms\n"
        "  Week 9: Transformers & BERT\n"
        "  Week 10: Agentic AI & LLM Applications\n\n"
        "Rules:\n"
        '- If the question is about course content/topics/lectures → route = "retrieve"\n'
        '- If general knowledge, math, greeting, or off-topic → route = "direct_answer"\n'
        "- If you can identify the week, set week to its number; otherwise set week to \"all\".\n\n"
        'Respond ONLY with valid JSON: {"route":"retrieve" or "direct_answer","week":"<number or all>","reason":"brief reason"}'
    )

    resp = llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=state["query"]),
    ]).content.strip()

    try:
        clean = resp.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)
        route = data.get("route", "direct_answer")
        week = str(data.get("week", "all"))
        reason = data.get("reason", "")
    except (json.JSONDecodeError, AttributeError):
        route, week, reason = "direct_answer", "all", "Could not parse routing response"

    trace = list(state.get("trace", []))
    trace.append({
        "node": "router",
        "detail": f"Route → {route} | Week → {week} | Reason: {reason}",
    })

    return {**state, "route": route, "week": week, "reason": reason, "trace": trace}


def retrieve_node(state: QueryState) -> dict:
    """Pull relevant week's notes from the knowledge base."""
    week_str = state.get("week", "all")
    if week_str.isdigit():
        week_num = int(week_str)
        notes = get_notes_for_week(week_num)
        if notes is None:
            notes = get_all_notes()
            detail = f"Week {week_num} not found — retrieved all weeks"
        else:
            detail = f"Retrieved notes for Week {week_num}"
    else:
        notes = get_all_notes()
        detail = "No specific week detected — retrieved all weeks"

    trace = list(state.get("trace", []))
    trace.append({"node": "retrieve", "detail": detail})
    return {**state, "context": notes, "trace": trace}


def direct_answer_node(state: QueryState) -> dict:
    """Skip retrieval — no course notes needed."""
    trace = list(state.get("trace", []))
    trace.append({
        "node": "direct_answer",
        "detail": "No retrieval needed — answering directly",
    })
    return {**state, "context": "", "trace": trace}


def generate_node(state: QueryState) -> dict:
    """Generate final answer using retrieved context (if any)."""
    if state.get("context"):
        system = (
            "You are Parishiksha, an AI/ML course teaching assistant.\n"
            "Answer the student's question using ONLY the course notes provided below.\n"
            "Be helpful, clear, and concise. If the notes don't cover the topic, say so.\n\n"
            f"--- COURSE NOTES ---\n{state['context']}\n--- END NOTES ---"
        )
    else:
        system = (
            "You are Parishiksha, a friendly AI assistant.\n"
            "The question is not about course content, so answer it directly.\n"
            "Be helpful and concise."
        )

    resp = llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=state["query"]),
    ]).content.strip()

    trace = list(state.get("trace", []))
    trace.append({"node": "generate", "detail": "Generated final response"})
    return {**state, "response": resp, "trace": trace}


# ──────────────── Build LangGraph ────────────────

def route_after_router(state: QueryState) -> str:
    """Conditional edge: send to retrieve or direct_answer based on router output."""
    return "retrieve" if state["route"] == "retrieve" else "direct_answer"


workflow = StateGraph(QueryState)
workflow.add_node("router", router_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("direct_answer", direct_answer_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("router")
workflow.add_conditional_edges("router", route_after_router, {
    "retrieve": "retrieve",
    "direct_answer": "direct_answer",
})
workflow.add_edge("retrieve", "generate")
workflow.add_edge("direct_answer", "generate")
workflow.add_edge("generate", END)

graph = workflow.compile()


# ──────────────── Flask Routes ────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Process a query through the LangGraph pipeline and stream results via SSE."""
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Empty query"}), 400

    def stream():
        """Run graph step-by-step, yielding SSE events for each node."""
        initial = QueryState(
            query=query, route="", week="", reason="",
            context="", response="", trace=[],
        )

        prev_trace_len = 0
        for event in graph.stream(initial, stream_mode="updates"):
            # event is {node_name: state_update}
            for node_name, update in event.items():
                trace = update.get("trace", [])
                # Emit new trace entries
                for entry in trace[prev_trace_len:]:
                    sse = json.dumps({"type": "node", **entry})
                    yield f"data: {sse}\n\n"
                prev_trace_len = len(trace)

                # If this node produced a response, emit it
                if "response" in update and update["response"]:
                    sse = json.dumps({
                        "type": "response",
                        "content": update["response"],
                    })
                    yield f"data: {sse}\n\n"

        yield "data: {\"type\":\"done\"}\n\n"

    return Response(stream(), mimetype="text/event-stream")


@app.route("/weeks")
def weeks():
    return jsonify(get_available_weeks())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
