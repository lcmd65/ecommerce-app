const search_bar = document.querySelector(".item-entry-search");
const button_search_bar = document.querySelector(".item-button-search-btn");

function renderProductCard(product) {
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
    eventClickedItemBase(buy);
    productCard.appendChild(buy);
    return productCard;
}

async function eventClickedItemBase(itemClick) {
    // Clear item click view
    itemClick.addEventListener("click", async function() {
        const workspaceContainer = document.querySelector(".main-workspace-container-header");
        while (workspaceContainer.firstChild) {
            workspaceContainer.removeChild(workspaceContainer.firstChild);
        }

        // Item click
        const item = document.createElement("div");
        item.classList.add("item-view-container");

        const barbutton = document.createElement("div");
        barbutton.classList.add("item-view-container-line-button");

        let itemButtonClose = document.createElement("button");
        itemButtonClose.classList.add("button-close-item-view");
        const imagePath = "/static/images/close.png";
        // Creating the image element
        const imageElement = document.createElement("img");
        imageElement.src = imagePath;
        itemButtonClose.appendChild(imageElement);
        itemButtonClose.addEventListener("click", function() {
            while (workspaceContainer.firstChild) {
                workspaceContainer.removeChild(workspaceContainer.firstChild);
            }
            workspaceContainer.style.height = "0px";
        });
        barbutton.appendChild(itemButtonClose);
        item.appendChild(barbutton);

        const content = document.createElement("div");
        content.classList.add("item-view-container-line");

        const itemName = document.createElement("p");
        itemName.innerHTML = itemClick.getAttribute("name");
        content.appendChild(itemName);

        const item_id = itemClick.getAttribute("id");
        const itemDescription = document.createElement("p");
        fetch('/description_get', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ item_id })
            })
            .then(response => response.json())
            .then(description => {
                itemDescription.textContent = description;
                content.appendChild(itemDescription);
            });

        item.appendChild(content);
        const barButtonCard = document.createElement("div");
        barButtonCard.classList.add("item-view-container-line-button-cart");

        let buttonCart = document.createElement("button");
        buttonCart.classList.add("button-cart");
        buttonCart.innerHTML = "Buy Now!";

        buttonCart.addEventListener("click", function() {
            fetch('/login', {
                method: "GET",
            });
            window.location.href = '/login';
        });

        barButtonCard.appendChild(buttonCart);
        item.appendChild(barButtonCard);
        workspaceContainer.appendChild(item);
        workspaceContainer.style.height = "300px";
    });
}

function renderWorkspaceSearch(data_render) {
    const workspace = document.querySelector(".main-workspace-container-body");
    while (workspace.firstChild) {
        workspace.removeChild(workspace.firstChild);
    }
    data_render.forEach(element => {
        const productCard = renderProductCard(element);
        workspace.appendChild(productCard);
    });
}

async function searchEvent() {
    const search_message = search_bar.value.trim();
    const request = await fetch("/search_2vec", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ search_message }),
    });

    const list_id = await request.json();
    const request_product = await fetch("/product_get", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ list_id }),
    });
    const productData = await request_product.json();
    renderWorkspaceSearch(productData);
}

button_search_bar.addEventListener("click", searchEvent);
search_bar.addEventListener("keydown", event => {
    if (event.keyCode === 13 && !event.shiftKey) {
        searchEvent();
    }
});