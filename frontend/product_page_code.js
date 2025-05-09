// Sample product data
const sample_products = [
    {
        name: "T-shirt 1",
        image_url: "/static/images/tshirt_1.jpg",
        description: "A comfortable cotton t-shirt.",
        likes: 0,
        price: 19.99,
    },
    {
        name: "T-shirt 2",
        image_url: "/static/images/tshirt_2.jpg",
        description: "A stylish t-shirt with a unique design.",
        likes: 0,
        price: 19.99,
    },
    {
        name: "T-shirt 3",
        image_url: "/static/images/tshirt_3.jpg",
        description: "A classic white t-shirt.",
        likes: 0,
        price: 19.99,
    },
    {
        name: "T-shirt 4",
        image_url: "/static/images/tshirt_4.jpg",
        description: "A trendy black t-shirt.",
        likes: 0,
        price: 19.99,
    },
    {
        name: "T-shirt 5",
        image_url: "/static/images/tshirt_5.jpg",
        description: "A vibrant red t-shirt.",
        likes: 0,
        price: 19.99,
    },
    {
        name: "T-shirt 6",
        image_url: "/static/images/tshirt_6.jpg",
        description: "A cool blue t-shirt.",
        likes: 0,
        price: 19.99,
    },
    {
        name: "T-shirt 7",
        image_url: "/static/images/tshirt_7.jpg",
        description: "A stylish green t-shirt.",
        likes: 0,
        price: 19.99,
    }
];

// Function to display products
function displayProducts(products) {
    const productList = document.querySelector('.products-list');
    productList.innerHTML = ''; // Clear existing products

    products.forEach(product => {
        const li = document.createElement('li');
        li.className = 'product-item';
        li.innerHTML = `
            <img src="/backend${product.image_url}" alt="${product.name}" />
            <h2>${product.name}</h2>
            <p class="product-description">${product.description}</p>
            <div class="product-likes-price">
                <p class="product-likes">❤️ ${product.likes}</p>
                <p class="product-price">${product.price.toFixed(2)}€</p>
            </div>
        `;
        productList.appendChild(li);
    });
}

// Initial display of all products
//displayProducts(sample_products);

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector(".search-bar input");
    const searchButton = document.querySelector(".search-bar button");

    searchButton.addEventListener("click", function () {
        const query = searchInput.value.trim();
        if (query) {
            fetch(`/search?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(products => {
                    productsList.innerHTML = ""; // Clear previous results
                    displayProducts(products);
                })
                .catch(error => console.error("Error fetching products:", error));
        }
    });
});