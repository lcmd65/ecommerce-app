async function eventClickedCart() {
    const workspace = document.querySelector(".main-workspace-container-header");
    while (workspace.firstChild) {
        workspace.removeChild(workspace.firstChild);
    }
    workspace.style.height = "760px";

    const message = await fetch("/cart_get", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        }
    });

    const response = await message.json();
    const item_list = response.item;

    const cart = document.createElement("div");
    cart.classList.add("cart-container");

    for (const item_id of item_list) {
        if (item_id !== "") {
            const request_item_data = await fetch("/item_get", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ item_id })
            });
            const item_data = await request_item_data.json();
            const cart_item = document.createElement("div");
            cart_item.classList.add("cart-item-container");
            const cart_item_name = document.createElement("div");
            cart_item_name.classList.add("cart-item-attribute");
            cart_item_name.innerHTML = item_data.name;
            cart_item.appendChild(cart_item_name);

            const item_price = document.createElement("div");
            item_price.classList.add("cart-item-attribute");
            item_price.innerHTML = "Price: " + item_data.price;
            cart_item.appendChild(item_price);

            const item_number_data = document.createElement("div");
            item_number_data.classList.add("cart-item-attribute");
            item_number_data.innerHTML = "Number of this product";

            var input_number_product = document.createElement('input');
            input_number_product.type = 'text';
            input_number_product.value = 1;
            input_number_product.id = item_id;
            input_number_product.classList.add('form-control');
            input_number_product.placeholder = "";
            item_number_data.appendChild(input_number_product);
            cart_item.appendChild(item_number_data);

            var checkbox = document.createElement('input');
            checkbox.classList.add("checkbox-item");
            checkbox.type = 'checkbox';
            checkbox.id = item_id;
            cart_item.appendChild(checkbox);

            cart.appendChild(cart_item);
        }
    }

    const button_bar = document.createElement("div");
    button_bar.classList.add("button-bar-cart");

    const button_destroy_items = document.createElement("button");
    button_destroy_items.classList.add("button-cart-items");
    button_destroy_items.innerHTML = "Delete Items";
    button_destroy_items.type = "submit";
    button_destroy_items.addEventListener("click", async function() {
        const checkbox_items = document.querySelectorAll(".checkbox-item");
        checkbox_items.forEach(async check_box => {
            if (check_box.checked) {
                const id = check_box.id;
                const request = await fetch("/item_del", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ id })
                });
                const response = await request.text();
                if (response === "1") {
                    messageBoxClient("Success");
                } else {
                    messageBoxClient("Fail");
                }
            }
        });
    });

    const button_buy = document.createElement("button");
    button_buy.classList.add("button-cart-items");
    button_buy.innerHTML = " Buy ";
    button_buy.addEventListener("click", async function() {

    });

    button_bar.appendChild(button_destroy_items);
    button_bar.appendChild(button_buy);

    const button_destroy = document.createElement("button");
    button_destroy.classList.add("button-cart-destroy");
    button_destroy.innerHTML = "Close";
    button_destroy.addEventListener("click", async function() {
        while (workspace.firstChild) {
            workspace.removeChild(workspace.firstChild);
        }
        workspace.style.height = "0px";
        workspace.style.width = "100%";
    });
    workspace.appendChild(cart);
    workspace.appendChild(button_bar);
    workspace.appendChild(button_destroy);
}

window.addEventListener('load', function() {
    const cartLink = document.querySelector(".cart-button-click");
    cartLink.addEventListener("click", eventClickedCart);
});