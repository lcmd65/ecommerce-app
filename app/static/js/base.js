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