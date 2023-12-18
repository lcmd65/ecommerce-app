function renderProductCardHome(product) {
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

    let buy = document.createElement("button");
    buy.classList.add("button-buy");
    buy.setAttribute("id", product._id);
    buy.setAttribute("name", product.name);
    buy.innerHTML = "Buy";
    eventClickedItemHome(buy);
    productCard.appendChild(buy);
    return productCard;
}

async function render_item_main_workspace(id) {
    const workspace = document.querySelector("main-workspace-container-header");
    while (workspace.firstChild) {
        workspace.removeChild(workspace.firstChild);
    }
    let item_id = id;
    const request = await fetch("item_get", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(item_id)
    })

    const respone = await request.json()
    render_item_recommend(respone)
}

async function render_item_recommend(item_data) {
    const chatbox_container = document.querySelector(".chat-box");
    const bot_message_recommend = document.createElement("bot-message");
    const item = document.createElement("div");
    item.classList.add("item-recommend");
    item_data.forEach(element => {
        const item = document.createElement("div");
        item.innerHTML = element.name;

        const item_price = document.createElement("p");
        item_price.innerHTML = element.price;

        const item_buy_button = document.createElement("p");
        item_buy_button.innerHTML = "Buy Now";
        item_buy_button.addEventListener("click", function() {
            render_item_main_workspace(item_data._id);
        })

        item.appendChild(item_price);
        item.appendChild(item_buy_button);
        bot_message_recommend.appendChild(item);
        chatbox_container.appendChild(bot_message_recommend);
    });
    item.innerHTML = item_data.name;
}