const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");

// Handle submit
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const message = userInput.value.trim();
  if (!message) return;

  // Add user message
  appendMessage(message, "user");
  userInput.value = "";

  // Add loading message
  const loadingMsg = appendMessage("Thinking...", "bot");

  try {
    const reply = await getGeminiReply(message);
    loadingMsg.textContent = reply;
  } catch (error) {
    loadingMsg.textContent = "⚠️ Error fetching response.";
    console.error(error);
  }
});

// Add message to chat
function appendMessage(text, sender) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);
  msgDiv.textContent = text;

  chatBox.appendChild(msgDiv);

  // Scroll to bottom always
  chatBox.scrollTop = chatBox.scrollHeight;

  return msgDiv;
}

// Backend call
async function getGeminiReply(prompt) {
  const response = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: prompt }),
  });

  const data = await response.json();
  return data.reply || "No response.";
}
