// Function to display products
function displayProducts(products) {
	const productList = document.querySelector('.products-list');
	productList.innerHTML = ''; // Clear existing products

	products.forEach(product => {
		//For every product fetched, an html element is created
		const li = document.createElement('li');
		li.className = 'product-item';
		li.dataset.id = product._id;
		li.innerHTML = `
            <img src="${product.image_url}" alt="${product.name}" />
            <h2>${product.name}</h2>
            <p class="product-description">${product.description}</p>
            <div class="product-likes-price">
                <p class="product-likes">❤️ ${product.likes}</p>
                <p class="product-price">${product.price.toFixed(2)}€</p>
            </div>
        `;

		//Update the likes property of a product if clicked
		li.addEventListener("click", function() {
			const productId = this.dataset.id;

			fetch(`/api/like`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
      			body: JSON.stringify({ _id: productId })
			})
			.then(response => response.json())
			.then(data => {
				if(data.success) {
					const likesElement = li.querySelector(".product-likes");
					likesElement.textContent = `❤️ ${data.updated_likes}`
				} else {
					console.error("Failed to update likes count");
				}
			})
			.catch(error => console.error("Failed to send like",error))
		})

		productList.appendChild(li);
	});
}

function triggerrSearch() {
	const query = document.querySelector(".search-bar input").value.trim();
	fetch(`/api/search?q=${encodeURIComponent(query)}`)
		.then(response => response.json())
		.then(products => {
			//Clearing not-found div
			const div = document.getElementById('not-found');
			div.innerHTML = '';

			//Show appropriate message if no products is matching the query
			if (products.length === 0){
				const p = document.createElement('p');

				p.textContent = `There are no products named "${query}"`;
				div.appendChild(p);
			}

			displayProducts(products);
			
		})
		.catch(error => console.error("Error fetching products:", error));
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

	searchButton.addEventListener("click", triggerrSearch());

	searchInput.addEventListener("keypress", function(event) {
		if (event.key == "Enter") {
			triggerrSearch();
		}
	})
});