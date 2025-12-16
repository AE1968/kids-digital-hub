// ============================================
// PRODUCT DATABASE (Simulated for Demo)
// ============================================

// Product Database (Live - Full 30 Items)
var allProducts = [
    // --- COLORING (10 Items) ---
    { id: "col-001", name: "Space Adventure Dog", category: "Coloring", is_free: true, image: "assets/images/products/space_dog.png", description: "Join the brave astronaut puppy on a mission to the stars!", link: "assets/images/products/space_dog.png" },
    { id: "col-002", name: "Dino Safari Jeep", category: "Coloring", is_free: true, image: "assets/images/products/dino_safari.png", description: "Beep beep! T-Rex is driving through the jungle.", link: "assets/images/products/dino_safari.png" },
    { id: "col-003", name: "Magical Unicorn Castle", category: "Coloring", is_free: true, image: "assets/images/products/unicorn.png", description: "Fly over the rainbow with this magical unicorn.", link: "assets/images/products/unicorn.png" },
    { id: "col-004", name: "Underwater Octopus", category: "Coloring", is_free: true, image: "assets/images/products/octopus.png", description: "Deep dive with Mr. Octopus as he juggles shells!", link: "assets/images/products/octopus.png" },
    { id: "col-005", name: "Friendly Garden Robot", category: "Coloring", is_free: true, image: "assets/images/products/robot.png", description: "Beep boop! This friendly robot loves nature.", link: "assets/images/products/robot.png" },
    { id: "col-006", name: "Mandala for Focus", category: "Coloring", is_free: true, image: "assets/images/logo_ae.png", description: "Simple mandala to help kids relax and focus.", link: "#" },
    { id: "col-007", name: "Superhero City", category: "Coloring", is_free: true, image: "assets/images/logo_ae.png", description: "Color the skyline and save the day!", link: "#" },
    { id: "col-008", name: "Princess Tea Party", category: "Coloring", is_free: true, image: "assets/images/logo_ae.png", description: "You are invited to the royal tea party.", link: "#" },
    { id: "col-009", name: "Farm Animals Fun", category: "Coloring", is_free: true, image: "assets/images/logo_ae.png", description: "Cows, pigs, and chickens waiting for colors.", link: "#" },
    { id: "pack-001", name: "🦄 Mega Variety Pack (50+)", category: "Coloring", is_free: false, image: "assets/images/products/pack_variety.png", description: "The ultimate collection! Dinos, Unicorns, Space & more.", link: "login.html?redirect=premium" },

    // --- STORIES (10 Items) ---
    { id: "sty-001", name: "Goodnight Moon Bear", category: "Stories", is_free: true, image: "assets/images/products/story_moon.png", description: "A soothing bedtime story about a sleepy bear.", link: "#" },
    { id: "sty-002", name: "Dino Learns to Share", category: "Stories", is_free: true, image: "assets/images/products/story_dino.png", description: "Rex the Dino discovers that sharing is caring.", link: "#" },
    { id: "sty-003", name: "Mermaid's First School Day", category: "Stories", is_free: true, image: "assets/images/products/story_mermaid.png", description: "Marina acts brave on her first day at Coral School.", link: "#" },
    { id: "sty-004", name: "The Polite Dragon", category: "Stories", is_free: true, image: "assets/images/logo_ae.png", description: "Drake learns magic words like Please and Thank You.", link: "#" },
    { id: "sty-005", name: "Lost Kitten Adventure", category: "Stories", is_free: true, image: "assets/images/logo_ae.png", description: "Help Fluffy find her way back home.", link: "#" },
    { id: "sty-006", name: "Space Picnic", category: "Stories", is_free: true, image: "assets/images/logo_ae.png", description: "Lunch on the moon? Why not!", link: "#" },
    { id: "sty-007", name: "The Boy Who Could Fly", category: "Stories", is_free: true, image: "assets/images/logo_ae.png", description: "A dream comes true in the clouds.", link: "#" },
    { id: "sty-008", name: "Forest Mystery", category: "Stories", is_free: true, image: "assets/images/logo_ae.png", description: "Who took the acorn? Owl Detective investigates.", link: "#" },
    { id: "sty-009", name: "Robot's Heart", category: "Stories", is_free: true, image: "assets/images/logo_ae.png", description: "Can a robot feel love? A touching tale.", link: "#" },
    { id: "pack-002", name: "🎧 Golden Audio Collection (20+)", category: "Stories", is_free: false, image: "assets/images/products/story_audio_pack.png", description: "Listen to magical stories anytime, anywhere.", link: "login.html?redirect=premium" },

    // --- GAMES (10 Items) ---
    { id: "gm-001", name: "Rabbit Maze Run", category: "Games", is_free: true, image: "assets/images/logo_ae.png", description: "Help the bunny find the carrot field! (Easy)", link: "#" },
    { id: "gm-002", name: "Jungle Detective", category: "Games", is_free: true, image: "assets/images/logo_ae.png", description: "Find 5 hidden monkeys in the picture.", link: "#" },
    { id: "gm-003", name: "Fruit Sudoku", category: "Games", is_free: true, image: "assets/images/logo_ae.png", description: "Logic puzzle with apples and bananas.", link: "#" },
    { id: "gm-004", name: "Connect the Dots: Cat", category: "Games", is_free: true, image: "assets/images/logo_ae.png", description: "Reveal the hidden pet by connecting 1-20.", link: "#" },
    { id: "gm-005", name: "Space Memory Cards", category: "Games", is_free: true, image: "assets/images/logo_ae.png", description: "Printable memory game with planets.", link: "#" },
    { id: "gm-006", name: "Math Coloring", category: "Games", is_free: true, image: "assets/images/logo_ae.png", description: "Solve 2+2 to know which color to use.", link: "#" },
    { id: "gm-007", name: "Shadow Match Dino", category: "Games", is_free: true, image: "assets/images/logo_ae.png", description: "Match the T-Rex to its shadow.", link: "#" },
    { id: "gm-008", name: "Word Search: Summer", category: "Games", is_free: true, image: "assets/images/logo_ae.png", description: "Find words like SUN, SEA, SAND.", link: "#" },
    { id: "gm-009", name: "Origami Starter", category: "Games", is_free: true, image: "assets/images/logo_ae.png", description: "Instructions to fold a paper boat.", link: "#" },
    { id: "pack-003", name: "🧩 Activity Book Giant (200pgs)", category: "Games", is_free: false, image: "assets/images/logo_ae.png", description: "Mazes, Puzzles, Math & More! The ultimate boredom stick.", link: "login.html?redirect=premium" }
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