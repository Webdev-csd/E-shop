// Function to display products
function displayProducts(products) {
	const productList = document.querySelector('.products-list');
	productList.innerHTML = ''; // Clear existing products

	products.forEach(product => {
		const li = document.createElement('li');
		li.className = 'product-item';
		li.innerHTML = `
            <img src="${product.image_url}" alt="${product.name}" />
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


document.addEventListener("DOMContentLoaded", function () {
	const query = "";
	fetch(`/api/search?q=${encodeURIComponent(query)}`)
		.then(response => response.json())
		.then(products => {
			displayProducts(products);
		})
		.catch(error => console.error("Error fetching products:", error));


	const searchInput = document.querySelector(".search-bar input");
	const searchButton = document.querySelector(".search-bar button");


	// Define the API URL
	searchButton.addEventListener("click", function () {
		const query = searchInput.value.trim();
		fetch(`/api/search?q=${encodeURIComponent(query)}`)
			.then(response => response.json())
			.then(products => {
				displayProducts(products);
			})
			.catch(error => console.error("Error fetching products:", error));
	});
});