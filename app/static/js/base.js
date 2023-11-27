async function addimage(image_src, productImage) {
    const image = document.createElement("img");
    image.src = image_src;
    image.height = 50;
    productImage.appendChild(image);
}

function renderProductCard(product) {
    //_id
    //name
    //description
    //availability
    //brand
    //color
    //currency
    //price
    //avg_rating
    //review_count
    //scraped_at
    //url
    const productCard = document.createElement("div");
    productCard.classList.add("product-card");

    const productImage = document.createElement("div");
    productImage.classList.add("product-image");
    //addimage(product.image, productImage);
    productCard.appendChild(productImage);

    const productName = document.createElement("p");
    productName.textContent = product.name;
    productCard.appendChild(productName);

    const productPrice = document.createElement("p");
    productPrice.textContent = `Price: ${product.price} ${product.currency}`;
    productCard.appendChild(productPrice);

    const productBrand = document.createElement("p");
    productBrand.textContent = `Brand: ${product.brand}`;
    productCard.appendChild(productBrand);

    const buy = document.createElement("button");
    buy.type = "submit"; // Set the button type to "submit"
    buy.value = product._id;
    buy.innerHTML = "Buy"; // Corrected syntax for setting inner HTML
    productCard.appendChild(buy);

    return productCard;
}

function renderWorkspace(data_render) {
    const workspace = document.querySelector(".main-workspace-container-body");
    data_render.forEach(element => {
        const productCard = renderProductCard(element);
        workspace.appendChild(productCard);
    });
}
async function renderProductView() {
    const response = await fetch("/product", method = ['GET']);
    const productDataText = await response.text();
    const productData = JSON.parse(productDataText);
    renderWorkspace(productData);
    chatInit();
}

window.addEventListener("load", renderProductView);

function changeHeightClose() {
    const box = document.querySelector(".chat-box-container");
    // Check the current height and toggle between 400px and 25px
    // Check the current height and toggle between 400px and 25px
    box.style.height = "25px";
}


function changeHeightOpen() {
    const box = document.querySelector(".chat-box-container");
    // Check the current height and toggle between 400px and 25px
    box.style.height = "400px";
}

const clickHeightOpen = document.querySelector("chat-button-openbutton")
const clickHeightClose = document.querySelector("chat-button-closebutton")

clickHeightClose.addEventListener("click", changeHeightClose);
clickHeightOpen.addEventListener("click", changeHeightOpen);

const chatBox = document.querySelector(".chat-box");
const chatContainer = document.querySelector(".chat-box-container");
const messageInput = document.querySelector("#message-input");
const sendBtn = document.querySelector("#send-btn");

function chatInit() {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("mt-3", "p-3", "rounded");
    messageDiv.classList.add("bot-message");
    messageDiv.innerHTML = `<img src="{{ url_for('static',filename='images/icons-bot.png') }}" class="bot-icon"><p>Please describe the product you are looking for</p>`;
    chatBox.appendChild(messageDiv);

    // Scroll the chat box to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

window.addEventListener("load", chatInit);

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