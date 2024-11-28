async function fetchProducts(query, n) {
    const apiUrl = `http://localhost:8000/search?q=${encodeURIComponent(query)}&n=${n}`;
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
      const payload = product.payload;
      const productCard = `
        <div class="product-card">
          <img src="${payload.images[0]}" alt="${payload.name}" />
          <h3>${payload.name}</h3>
          <p>${payload.current_price} ${payload.currency}</p>
          <a>View Product</a>
        </div>
      `;
      productGrid.innerHTML += productCard;
    });
  }
  
  document.getElementById("searchButton").addEventListener("click", async () => {
    const query = document.getElementById("searchInput").value.trim();
    if (!query) {
      alert("Please enter a search term.");
      return;
    }
  
    const products = await fetchProducts(query, 10);
    renderProducts(products);
  });
  