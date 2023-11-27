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


document.addEventListener("DOMContentLoaded", async function() {
    fetch('/product')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Check if the 'product_data' property exists in the response
            if (data && data.product_data) {
                const productData = data.product_data;
                // Now you can use productData in your JavaScript logic
                console.log(productData);
            } else {
                console.error('Invalid product data format:', data);
            }
        })
        .catch(error => console.error('Error fetching product data:', error));

    // Function to render the product card
    function renderProductCard(product) {
        // Create HTML elements for the product card
        const productCard = document.createElement("div");
        productCard.classList.add("product-card");

        const productName = document.createElement("h2");
        productName.textContent = product.name;
        productCard.appendChild(productName);

        const productPrice = document.createElement("p");
        productPrice.textContent = `Price: ${product.price}`;
        productCard.appendChild(productPrice);

        const productDescription = document.createElement("p");
        productDescription.textContent = product.description;
        productCard.appendChild(productDescription);

        const productImage = document.createElement("img");
        productImage.src = product.imageUrl;
        productImage.alt = "Product Image";
        productCard.appendChild(productImage);

        return productCard;
    }

    function renderWorkspace(product_data_render) {
        const workspace = document.querySelector(".container-body");
        for (const product of product_data_render) {
            const productCard = renderProductCard(product);
            workspace.appendChild(productCard);
        }
    }

    renderWorkspace(productData);
});