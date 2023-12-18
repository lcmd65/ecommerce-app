const itemProduct = document.querySelectorAll(".button-buy");

function eventClickedItem(itemClick) {
    // Clear item click view
    const workspaceContainer = document.querySelector(".main-workspace-container-header");
    while (workspaceContainer.firstChild) {
        workspaceContainer.removeChild(workspaceContainer.firstChild);
    }

    // Item click
    const item = document.createElement("div");
    item.classList.add("item-view-container");

    const itemName = document.createElement("p");
    itemName.classList.add("item-view-container-line");
    itemName.innerHTML = itemClick.name;
    item.appendChild(itemName);

    const _id = itemClick.value;
    const itemDescription = document.createElement("p");
    itemDescription.classList.add("item-view-container-line");

    const request = fetch('/description_get', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ _id })
    });

    const response = request.json();
    itemDescription.innerHTML = JSON.parse(response);
    item.appendChild(itemDescription);

    const buttonCart = document.createElement("button");
    buttonCart.classList.add("button-card");
    buttonCart.innerHTML = "Add to cart";
    buttonCart.value = itemClick.value;

    buttonCart.addEventListener("click", async function() {
        const requestAdd = await fetch('/cart_add', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ _id })
        });
        const responseAdd = await requestAdd.json();
        if (responseAdd.success === true) {
            while (workspaceContainer.firstChild) {
                workspaceContainer.removeChild(workspaceContainer.firstChild);
            }
            const textMessage = document.createElement("p");
            textMessage.innerHTML = "Success";
            workspaceContainer.appendChild(textMessage);
            const buttonDestroy = document.createElement("button");
            buttonDestroy.innerHTML = "OK";
            buttonDestroy.addEventListener("click", async function() {
                while (workspaceContainer.firstChild) {
                    workspaceContainer.removeChild(workspaceContainer.firstChild);
                }
            });
            workspaceContainer.appendChild(buttonDestroy);
        } else {
            while (workspaceContainer.firstChild) {
                workspaceContainer.removeChild(workspaceContainer.firstChild);
            }
            const textMessage = document.createElement("p");
            textMessage.innerHTML = "Fail";
            workspaceContainer.appendChild(textMessage);
            const buttonDestroy = document.createElement("button");
            buttonDestroy.innerHTML = "OK";
            buttonDestroy.addEventListener("click", async function() {
                while (workspaceContainer.firstChild) {
                    workspaceContainer.removeChild(workspaceContainer.firstChild);
                }
            });
            workspaceContainer.appendChild(buttonDestroy);
        }
    });
    item.appendChild(buttonCart);
}

itemProduct.forEach(element => {
    element.addEventListener("click", () => eventClickedItem(element));
});