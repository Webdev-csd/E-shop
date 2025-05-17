const swiper = new Swiper('.swiper', {
			// Optional parameters
			direction: 'horizontal',
			autoplay: {
				delay: 3000,
				disableOnInteraction: false
			},
			loop: true,


			// If we need pagination
			pagination: {
				el: '.swiper-pagination',
				clickable: true,
			},

			// Navigation arrows
			navigation: {
				nextEl: '.swiper-button-next',
				prevEl: '.swiper-button-prev',
			},


		});

fetch(`/api/popular_products`)
    .then(response => response.json())
    .then(dataArray => {

        list = document.getElementById("slideshow")
        list.innerHTML = ""

        dataArray.forEach(product => {
            console.log(product)

            const slide = document.createElement("div")
            slide.className = "swiper-slide"

            const img = document.createElement("img")
            img.src = product.image_url
            img.alt = product.description

            slide.appendChild(img)
            list.appendChild(slide)
        })

        swiper.update()

    })
    .catch(error => console.error(error))
