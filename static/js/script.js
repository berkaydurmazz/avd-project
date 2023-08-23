const products = [
    { name: "telefon", price: 100 },
    { name: "Ürün 2", price: 200 },
    { name: "Ürün 3", price: 150 },
    // Daha fazla ürün eklenebilir
];

const searchButton = document.getElementById("search-button");
const productInput = document.getElementById("product-input");
const resultSection = document.getElementById("result-section");
const testimonialsContainer = document.getElementById("testimonials-container");
const carInput = document.getElementById("car-input");
const homeButton = document.getElementById("home-button");
const testimonialSection = document.getElementById("testimonial-section");

// Klavye dinleyicisi ekle
productInput.addEventListener("keyup", event => {
    if (event.key === "Enter") {
        performSearch();
    }
});

searchButton.addEventListener("click", performSearch);

function performSearch() {
    const productName = productInput.value.trim().toLowerCase();
    
    // Eğer sorgu boş ise
    if (productName === "") {
        alert("Lütfen bir ürün adı girin!");
    } else {
        const matchingProducts = products.filter(product =>
            product.name.toLowerCase().includes(productName)
        );
        
        displayResults(matchingProducts);
    }
}

function displayResults(products) {
    resultSection.innerHTML = "";
    if (products.length === 0) {
        resultSection.innerHTML = "<p>Ürün bulunamadı.</p>";
    } else {
        products.forEach(product => {
            const resultBox = document.createElement("div");
            resultBox.classList.add("result-box");
            resultBox.innerHTML = `<p>Ürün Adı: ${product.name}</p><p>Fiyat: ${product.price} TL</p>Ürün Hakkında Müşteri Yorumları`;
            resultSection.appendChild(resultBox);
        }); 
    }
}

const carData = [
    {
        name: "Mercedes",
        testimonials: [
            // ... Yorumlar ...
        ]
    },
    {
        name: "Volvo",
        testimonials: [
            // ... Yorumlar ...
        ]
    },
    {
        name: "BMW",
        testimonials: [
            // ... Yorumlar ...
        ]
    },
    // Diğer arabalar
    {
        name: "Audi",
        testimonials: [
            // ... Yorumlar ...
        ]
    },
    {
        name: "Toyota",
        testimonials: [
            // ... Yorumlar ...
        ]
    },
    
    {
        name: "Ford",
        testimonials: [
            // ... Yorumlar ...
        ]
    },
    // Yeni arabalar buraya eklenir
];

homeButton.addEventListener("click", function() {
    clearResults();
    clearTestimonials();
    location.reload(); // Sayfayı yeniden yükle
});

searchButton.addEventListener("click", function() {
    const enteredCar = carInput.value.trim();

    // Araba sorgusu için API isteği yapabilirsiniz veya burada elinizdeki veriyi kullanabilirsiniz
    // Bu örnek için sabit bir veri kullanıyoruz
    const selectedCarData = carData.find(car => car.name.toLowerCase() === enteredCar.toLowerCase());

    // Sonuçları temizle
    resultSection.innerHTML = "";
    testimonialsContainer.innerHTML = "";

    if (selectedCarData) {
        // Arabaya ait yorumları ekrana ekleyin
        selectedCarData.testimonials.forEach(function(testimonial) {
            const testimonialDiv = document.createElement("div");
            testimonialDiv.className = "testimonial";
            testimonialDiv.innerHTML = `
                <p>"${testimonial.comment}"</p>
                <p class="testimonial-author">- ${testimonial.author}</p>
            `;
            testimonialsContainer.appendChild(testimonialDiv);
        });

        testimonialSection.style.display = "block"; // Yorumları göster
    } else {
        // Ürün bulunamadı mesajı ekleyin
        resultSection.innerHTML = "<p>Ürün bulunamadı.</p>";
        testimonialSection.style.display = "none"; // Yorumları gizle
    }
});

function clearResults() {
    resultSection.innerHTML = "";
}

function clearTestimonials() {
    testimonialsContainer.innerHTML = "";
}






