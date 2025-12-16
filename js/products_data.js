// ============================================
// PRODUCT DATABASE (Simulated for Demo)
// ============================================

// Product Database (Live)
var allProducts = [
    {
        id: "col-001",
        name: "Space Adventure Dog",
        category: "Coloring",
        is_free: true,
        image: "assets/images/products/space_dog.png",
        description: "Join the brave astronaut puppy on a mission to the stars! Perfect for little dreamers.",
        link: "assets/images/products/space_dog.png"
    },
    {
        id: "col-002",
        name: "Dino Safari Jeep",
        category: "Coloring",
        is_free: true,
        image: "assets/images/products/dino_safari.png",
        description: "Beep beep! T-Rex is driving through the jungle. A fun page for dino lovers.",
        link: "assets/images/products/dino_safari.png"
    },
    {
        id: "col-003",
        name: "Magical Unicorn Castle",
        category: "Coloring",
        is_free: true,
        image: "assets/images/products/unicorn.png",
        description: "Fly over the rainbow with this magical unicorn and her castle in the clouds.",
        link: "assets/images/products/unicorn.png"
    },
    {
        id: "col-004",
        name: "Underwater Octopus Party",
        category: "Coloring",
        is_free: true,
        image: "assets/images/products/octopus.png",
        description: "Deep dive with Mr. Octopus as he juggles shells! Fun and easy to color.",
        link: "assets/images/products/octopus.png"
    },
    {
        id: "col-005",
        name: "Friendly Garden Robot",
        category: "Coloring",
        is_free: true,
        image: "assets/images/products/robot.png",
        description: "Beep boop! This friendly robot loves nature. A great mix of tech and nature.",
        link: "assets/images/products/robot.png"
    },
    {
        id: "pack-001",
        name: "🦄 Mega Variety Pack (50+ Pages)",
        category: "Coloring",
        is_free: false,
        image: "assets/images/products/pack_variety.png",
        description: "The ultimate collection! Dinos, Unicorns, Space & more. Hours of fun guaranteed.",
        link: "login.html?redirect=premium"
    }
];

// ============================================
// RENDER ENGINE
// ============================================

function renderProducts(products) {
    const grid = document.getElementById('product-grid');
    if (!grid) {
        console.error("DEBUG: 'product-grid' element not found in DOM!");
        return;
    }

    // Clear current content
    grid.innerHTML = '';

    if (products.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: white;">
                <h2>🚫 No products found in this category.</h2>
                <p>Try switching categories or check back later!</p>
            </div>
        `;
        return;
    }

    products.forEach(product => {
        // Safe Image Handling
        const imgPath = product.image || 'assets/images/logo_ae.png';
        const badgeColor = product.is_free ? '#4CAF50' : '#FFD700'; // Green for Free, Gold for Premium
        const badgeText = product.is_free ? 'FREE' : 'PREMIUM';
        const badgeClass = product.is_free ? 'badge-free' : 'badge-premium';

        const card = document.createElement('div');
        card.className = 'product-card';
        // Add subtle animation delay
        card.style.animation = 'fadeInUp 0.5s ease forwards';

        card.innerHTML = `
            <div class="card-image-container">
                <span class="product-badge ${badgeClass}" style="background-color: ${badgeColor};">${badgeText}</span>
                <img src="${imgPath}" alt="${product.name}" onerror="this.src='assets/images/logo_ae.png'">
            </div>
            <div class="card-content">
                <div class="card-category">${product.category.toUpperCase()}</div>
                <h3 class="card-title">${product.name}</h3>
                <p class="card-desc">${product.description}</p>
                <div class="card-actions">
                    <a href="${product.link}" class="btn-card">View Item</a>
                </div>
            </div>
        `;

        grid.appendChild(card);
    });
}

// ============================================
// CSS INJECTION FOR DYNAMIC CARDS
// ============================================
// Ensuring styles exist even if CSS file is missing them
const style = document.createElement('style');
style.innerHTML = `
    .product-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        display: flex;
        flex-direction: column;
        border: 1px solid rgba(255,255,255,0.5);
    }
    .product-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    .card-image-container {
        height: 200px;
        position: relative;
        overflow: hidden;
        border-bottom: 5px solid #FFCCBC;
    }
    .card-image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s;
    }
    .product-card:hover .card-image-container img {
        transform: scale(1.1);
    }
    .product-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        padding: 5px 12px;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        font-size: 0.8rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 2;
    }
    .card-content {
        padding: 20px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    .card-category {
        font-size: 0.75rem;
        color: #E64A19;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .card-title {
        font-size: 1.2rem;
        color: #333;
        margin: 0 0 10px 0;
        font-weight: 700;
        line-height: 1.3;
    }
    .card-desc {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 20px;
        flex-grow: 1;
        line-height: 1.5;
    }
    .btn-card {
        display: block;
        width: 100%;
        padding: 12px;
        text-align: center;
        background: linear-gradient(135deg, #FF7043, #E64A19);
        color: white;
        text-decoration: none;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.2s;
    }
    .btn-card:hover {
        filter: brightness(1.1);
        transform: scale(1.02);
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);