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
    buy.classList.add("button-buy")
    buy.type = "submit"; // Set the button type to "submit"
    buy.id = product._id;
    buy.name = product.name;
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

async function chatInit() {
    const chatBox = document.querySelector(".chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("mt-3", "p-3", "rounded");
    messageDiv.classList.add("bot-message");
    messageDiv.innerHTML = `<img src="{{ url_for('static',filename='images/icons-bot.png') }}" class="bot-icon"><p>Please describe the product you are looking for</p>`;
    chatBox.appendChild(messageDiv);

    // Scroll the chat box to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function renderProductView() {
    const response = await fetch("/product", { method: "GET" });
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
window.addEventListener("load", renderProductView);