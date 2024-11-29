// async function fetchProducts(query, n) {
//     const apiUrl = `http://localhost:8000/search?q=${encodeURIComponent(query)}&n=${n}`;
//     try {
//       const response = await fetch(apiUrl);
//       if (!response.ok) throw new Error("Failed to fetch products.");
//       return await response.json();
//     } catch (error) {
//       console.error(error);
//       return [];
//     }
//   }
  
//   function renderProducts(products) {
//     const productGrid = document.getElementById("productGrid");
//     productGrid.innerHTML = ""; 
  
//     if (products.length === 0) {
//       productGrid.innerHTML = "<p>No products found</p>";
//       return;
//     }
  
//     products.forEach((product) => {
//       //const payload = product.payload;
//       const productCard = `
//         <div class="product-card">
//           <img src="${product.images[0]}" alt="${product.name}" />
//           <h3>${product.name}</h3>
//           <p>${product.current_price} ${product.currency}</p>
//           <a>View Product</a>
//         </div>
//       `;
//       productGrid.innerHTML += productCard;
//     });
//   }
  
//   document.getElementById("searchButton").addEventListener("click", async () => {
//     const query = document.getElementById("searchInput").value.trim();
//     if (!query) {
//       alert("Please enter a search term.");
//       return;
//     }
  
//     const products = await fetchProducts(query, 10);
//     renderProducts(products);
//   });
async function fetchProducts(query, n, proportion) {
  const apiUrl = `http://localhost:8000/search?q=${encodeURIComponent(query)}&n=${n}&p=${proportion}`;
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) throw new Error("Failed to fetch products.");
    return await response.json();
  } catch (error) {
    console.error(error);
    return [];
  }
}

function renderProducts(products) {
  const productGrid = document.getElementById("productGrid");
  productGrid.innerHTML = ""; 

  if (products.length === 0) {
    productGrid.innerHTML = "<p>No products found</p>";
    return;
  }

  products.forEach((product) => {
    const productCard = `
      <div class="product-card">
        <img src="${product.images[0]}" alt="${product.name}" />
        <h3>${product.name}</h3>
        <p>${product.current_price} ${product.currency}</p>
        <a>View Product</a>
      </div>
    `;
    productGrid.innerHTML += productCard;
  });
}

document.getElementById("proportionSlider").addEventListener("input", (event) => {
  const sliderValue = document.getElementById("sliderValue");
  sliderValue.textContent = event.target.value;
});

document.getElementById("searchButton").addEventListener("click", async () => {
  const query = document.getElementById("searchInput").value.trim();
  const proportion = document.getElementById("proportionSlider").value;
  if (!query) {
    alert("Please enter a search term.");
    return;
  }

  const products = await fetchProducts(query, 10, proportion);
  renderProducts(products);
});
