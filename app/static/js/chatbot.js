setInterval(highlightAll, 1000);
// Function to highlight code using highlight.js library
function highlightAll() {
    document.querySelectorAll("pre code").forEach(block => {
        hljs.highlightBlock(block);
    });
}

const chatBox = document.querySelector(".chat-box");
const chatContainer = document.querySelector(".chat-box-container");
const messageInput = document.querySelector("#message-input");
const sendBtn = document.querySelector("#send-btn");

function addMessage(message, isUserMessage) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("mt-3", "p-3", "rounded");

    if (isUserMessage) {
        messageDiv.classList.add("user-message");
    } else {
        messageDiv.classList.add("bot-message");
    }
    messageDiv.innerHTML = `<img src="{{ url_for('static',filename='images/icons-user.png') }}" class="user-icon"><p>${message}</p>`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (message !== "") {
        // Add a loading indicator
        const loadingIndicator = document.createElement("div");
        loadingIndicator.classList.add("loader");
        chatContainer.appendChild(loadingIndicator);
        // Add the user's message to the chat box
        addMessage(message, true);
        // Send the message to the bot
        try {
            const response = await fetch("/chat_api", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message }),
            });

            // Get the bot's response
            const data = await response.json();

            // Escape any HTML entities in the bot's response
            try {
                const escapedContent = data.content.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
                const data = escapedContent
            } catch (error) {
                console.error(error);
            }

            // Remove the loading indicator
            const loadingIndicator = document.querySelector(".loader");
            loadingIndicator.remove();

            // Add the bot's response to the chat box
            const messageDiv = document.createElement("div");
            messageDiv.classList.add("mt-3", "p-3", "rounded");
            messageDiv.classList.add("bot-message");
            messageDiv.innerHTML = `<img src="{{ url_for('static',filename='images/icons-bot.png') }}" class="bot-icon"><p>${data}</p>`;
            chatBox.appendChild(messageDiv);

            // Scroll the chat box to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            // Log the error
            console.error("Failed to fetch bot response:", error);

            // Show a more specific error message to the user
            const errorMessageDiv = document.createElement("div");
            errorMessageDiv.classList.add("mt-3", "p-3", "rounded");
            errorMessageDiv.classList.add("error-message");
            errorMessageDiv.innerHTML = `<p>Oops, something went wrong while fetching the bot response: ${error.message}</p>`;
            chatBox.appendChild(errorMessageDiv);

            // Remove the loading indicator even if there is an error
            const loadingIndicator = document.querySelector(".loader");
            loadingIndicator.remove();
        }
        // Clear the message input
        messageInput.value = "";
    }
}

sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keydown", event => {
    if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});