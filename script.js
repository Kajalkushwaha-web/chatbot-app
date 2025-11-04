const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  // Add user message to chat
  appendMessage(message, "user");
  userInput.value = "";

  // Placeholder loading message
  const loadingMsg = appendMessage("Thinking...", "bot");

  // Call Gemini API (pseudo-code)
  try {
    const reply = await getGeminiReply(message);
    loadingMsg.textContent = reply;
  } catch (error) {
    loadingMsg.textContent = "⚠️ Error fetching response.";
    console.error(error);
  }
});

function appendMessage(text, sender) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);
  msgDiv.textContent = text;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
  return msgDiv;
}

// Placeholder for Gemini API call
async function getGeminiReply(prompt) {
  // Replace YOUR_API_KEY and endpoint with your actual Gemini API info
  
  const response = await fetch("http://127.0.0.1:8000/chat",{
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message:prompt
    }),
  });

  const data = await response.json();
  return data.reply || "No response.";
}
