async function loadProducts() {
    const container = document.getElementById("product-container");

    try {
        const response = await fetch("products.json");
        const products = await response.json();

        products.forEach(product => {
            const card = document.createElement("div");
            card.className = "product-card";

            card.innerHTML = `
                <img src="${product.image}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p class="price">${product.price}</p>
            `;

            container.appendChild(card);
        });

    } catch (error) {
        console.error("Error loading products:", error);
    }
}

loadProducts();

// ----------------------
// IMAGE ZOOM ON CLICK
// ----------------------

const modal = document.getElementById("imgModal");
const modalImg = document.getElementById("modalImage");
const closeBtn = document.getElementsByClassName("close")[0];

function enableImageZoom() {
    const productImages = document.querySelectorAll(".product-card img");

    productImages.forEach(img => {
        img.addEventListener("click", () => {
            modal.style.display = "block";
            modalImg.src = img.src;
        });
    });
}

closeBtn.onclick = function () {
    modal.style.display = "none";
};

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

// Enable zoom AFTER products are loaded
setTimeout(enableImageZoom, 1000);