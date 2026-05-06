// ─── Parishiksha Frontend ───

const messagesEl  = document.getElementById("messages");
const chatForm    = document.getElementById("chatForm");
const queryInput  = document.getElementById("queryInput");
const sendBtn     = document.getElementById("sendBtn");
const traceLog    = document.getElementById("traceLog");
const graphPanel  = document.getElementById("graphPanel");
const pulseDot    = document.querySelector(".pulse-dot");

// ─── Graph node references ───
const GRAPH_NODES = ["router", "retrieve", "direct_answer", "generate"];

// Edge mapping: which edges to highlight when a node activates
const EDGE_MAP = {
  router:        ["edge-router-retrieve", "edge-router-direct"],
  retrieve:      ["edge-retrieve-generate"],
  direct_answer: ["edge-direct-generate"],
  generate:      ["edge-generate-end"],
};

// ─── Reset graph visuals ───
function resetGraph() {
  GRAPH_NODES.forEach((id) => {
    const el = document.getElementById(`node-${id}`);
    if (el) el.classList.remove("active-processing", "active-done");
  });
  document.querySelectorAll(".edge").forEach((e) => e.classList.remove("edge-active"));
  // Keep the start edge active
  document.querySelector(".edge.edge-active")?.classList.add("edge-active");
}

// ─── Highlight a node ───
function activateNode(nodeId, state) {
  const el = document.getElementById(`node-${nodeId}`);
  if (!el) return;

  if (state === "processing") {
    el.classList.add("active-processing");
    el.classList.remove("active-done");
  } else {
    el.classList.remove("active-processing");
    el.classList.add("active-done");
    // Light up outgoing edges
    const edgeKey = nodeId;
    (EDGE_MAP[edgeKey] || []).forEach((eId) => {
      const edge = document.getElementById(eId);
      if (edge) edge.classList.add("edge-active");
    });
  }
}

// ─── Add trace log entry ───
function addTraceEntry(node, detail) {
  // Remove placeholder
  const placeholder = traceLog.querySelector(".trace-placeholder");
  if (placeholder) placeholder.remove();

  const entry = document.createElement("div");
  entry.className = "trace-entry";
  entry.innerHTML = `
    <span class="trace-node ${node}">${node}</span>
    <span class="trace-detail">${detail}</span>
  `;
  traceLog.appendChild(entry);
  traceLog.scrollTop = traceLog.scrollHeight;
}

// ─── Add message bubble ───
function addMessage(role, content) {
  const msg = document.createElement("div");
  msg.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = role === "bot" ? "🎓" : "U";

  const contentEl = document.createElement("div");
  contentEl.className = "message-content";

  // Simple markdown-ish rendering
  const formatted = content
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br>");
  contentEl.innerHTML = `<p>${formatted}</p>`;

  msg.appendChild(avatar);
  msg.appendChild(contentEl);
  messagesEl.appendChild(msg);
  messagesEl.scrollTop = messagesEl.scrollHeight;

  return contentEl;
}

// ─── Typing indicator ───
function showTyping() {
  const msg = document.createElement("div");
  msg.className = "message bot";
  msg.id = "typing-indicator";
  msg.innerHTML = `
    <div class="message-avatar">🎓</div>
    <div class="message-content">
      <div class="typing-dots"><span></span><span></span><span></span></div>
    </div>
  `;
  messagesEl.appendChild(msg);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function hideTyping() {
  const el = document.getElementById("typing-indicator");
  if (el) el.remove();
}

// ─── Send query ───
async function sendQuery(query) {
  if (!query.trim()) return;

  // UI state
  sendBtn.disabled = true;
  queryInput.disabled = true;
  addMessage("user", query);
  resetGraph();

  // Clear previous trace
  traceLog.innerHTML = "";
  graphPanel.classList.add("active");
  pulseDot.classList.add("active");
  showTyping();

  try {
    const resp = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Process complete SSE lines
      const lines = buffer.split("\n");
      buffer = lines.pop(); // keep incomplete line in buffer

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const jsonStr = line.slice(6).trim();
        if (!jsonStr) continue;

        try {
          const event = JSON.parse(jsonStr);

          if (event.type === "node") {
            // Briefly show "processing" then "done"
            activateNode(event.node, "processing");
            addTraceEntry(event.node, event.detail);

            // Settle to done after a short delay
            setTimeout(() => activateNode(event.node, "done"), 400);
          }

          if (event.type === "response") {
            hideTyping();
            addMessage("bot", event.content);
          }

          if (event.type === "done") {
            // Activate end node
            const endNode = document.getElementById("node-end");
            if (endNode) endNode.classList.add("active-done");
          }
        } catch (e) {
          // ignore parse errors for partial lines
        }
      }
    }
  } catch (err) {
    hideTyping();
    addMessage("bot", `⚠️ Error: ${err.message}. Make sure the server is running.`);
  } finally {
    sendBtn.disabled = false;
    queryInput.disabled = false;
    queryInput.focus();
    pulseDot.classList.remove("active");

    // Keep panel highlighted briefly
    setTimeout(() => graphPanel.classList.remove("active"), 2000);
  }
}

// ─── Event listeners ───
chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const q = queryInput.value.trim();
  if (q) {
    sendQuery(q);
    queryInput.value = "";
  }
});

// Suggestion buttons
function askSuggestion(btn) {
  const q = btn.textContent.trim();
  queryInput.value = q;
  sendQuery(q);
  queryInput.value = "";
}

// Make askSuggestion globally accessible
window.askSuggestion = askSuggestion;
