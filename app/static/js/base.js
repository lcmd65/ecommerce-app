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

document.addEventListener("DOMContentLoaded", function() {
    // Access product_data variable passed from Flask
    const productData = window.productData;

    // Function to render the product card
    function renderProductCard(product, productCard) {
        // Create HTML elements for the product card
        const productName = document.createElement("h2");
        productName.textContent = product.name;

        const productPrice = document.createElement("p");
        productPrice.textContent = `Price: ${product.price}`;

        const productDescription = document.createElement("p");
        productDescription.textContent = product.description;

        const productImage = document.createElement("img");
        productImage.src = product.imageUrl;
        productImage.alt = "Product Image";

        // Append elements to the product card container
        productCard.appendChild(productName);
        productCard.appendChild(productPrice);
        productCard.appendChild(productDescription);
        productCard.appendChild(productImage);
    }


    function renderWorkspace(product_data_render) {
        const workspace = document.querySelector("container-body");
        for (const product of product_data_render) {
            const item = createElement("div");
            item.classList.add("product-card");
            renderProductCard(product, item);
            workspace.appendChild(item);
        }
    }
    renderWorkspace(productData);
});