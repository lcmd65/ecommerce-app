const item_product = document.querySelectorAll(".button-buy");

async function eventClickedItem(item_click) {
    // clear item click view
    const workspace_container = document.querySelector(".main-workspace-container-header");
    while (workspace_container.firstChild) {
        workspace_container.removeChild(workspace_container.firstChild);
    }

    // item click
    const item = document.createElement("div");
    item.classList.add("item-view-container");

    const item_name = document.createElement("p");
    item_name.classList.add("item-view-container-line");
    item_name.innerHTML = item_click.name;
    item.appendChild(item_name);

    const _id = item_click.value;
    const item_description = document.createElement("p");
    item_description.classList.add("item-view-container-line");

    const request = await fetch('/description_get', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ _id })
    });

    const respone = await request.json();
    item_description.innerHTML = JSON.parse(respone);
    item.appendChild(item_description);

    const button_cart = document.createElement("button");
    button_cart.classList.add("button-card");
    button_cart.innerHTML = "Add to cart";
    button_cart.value = item_click.value;
    item.appendChild(button_cart);

    button_cart.addEventListener("click", async function() {
        const request_add = await fetch('/cart_add', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ _id })
        });

        const respone_add = await request_add.text();
        if (respone_add === "True") {
            while (workspace_container.firstChild) {
                workspace_container.removeChild(workspace_container.firstChild);
            }
            const textmess = document.createElement("p");
            textmess.innerHTML = "Success";
            workspace_container.appendChild(textmess);
            const button_destroy = document.createElement("button");
            button_destroy.innerHTML = "OK";
            button_destroy.addEventListener("click", function() {
                while (workspace_container.firstChild) {
                    workspace_container.removeChild(workspace_container.firstChild);
                }
            });
            workspace_container.appendChild(button_destroy);
        } else {
            while (workspace_container.firstChild) {
                workspace_container.removeChild(workspace_container.firstChild);
            }
            const textmess = document.createElement("p");
            textmess.innerHTML = "Fail";
            workspace_container.appendChild(textmess);
            const button_destroy = document.createElement("button");
            button_destroy.innerHTML = "OK";
            button_destroy.addEventListener("click", function() {
                while (workspace_container.firstChild) {
                    workspace_container.removeChild(workspace_container.firstChild);
                }
            });
            workspace_container.appendChild(button_destroy);
        }
    });
}

item_product.forEach(element => {
    element.addEventListener("click", () => eventClickedItem(element));
});