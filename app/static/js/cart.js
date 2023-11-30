function eventClickedCart() {
    const body = document.querySelector("body");
    const message = fetch("/card_get", {
        method: "GET"
    });
    const respone = JSON.parse(message.json());
    const item = respone.item;

    const cart = document.createElement("div");
    cart.classList.add("cart-container");
    item.forEach(element => {
        const cart_item = document.createElement("div");
        cart_item.innerHTML = element;
        cart.appendChild(cart_item);
    });
    const button_destroy = document.createElement("button");
    button_destroy.innerHTML = "Close";
    button_destroy.addEventListener("click", function() {
        while (cart.firstChild) {
            cart.removeChild(cart.firstChild);
        }
        body.removeChild(cart);
    });
    cart.appendChild(button_destroy);
    body.appendChild(cart);
}

const cartIcon = document.querySelector("#card-icon");
cartIcon.addEventListener("click", eventClickedCart);