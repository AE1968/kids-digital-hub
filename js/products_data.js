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
    { id: "sty-001", name: "Goodnight Moon Bear", category: "Stories", is_free: true, image: "assets/images/products/story_moon.png", description: "A soothing bedtime story about a sleepy bear.", link: "story_goodnight_moon.html" },
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
// RENDER FUNCTION (Dynamic Product Display)
// ============================================

function renderProducts(products) {
    const grid = document.getElementById('product-grid');
    if (!grid) return;

    if (products.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">🔍</div>
                <h2 style="color: #666; font-family: 'Fredoka', sans-serif;">No products found</h2>
                <p style="color: #999;">Try selecting a different category or tier.</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = products.map(p => `
        <div class="product-card" style="animation: fadeInUp 0.6s ease;">
            <div class="product-badge ${p.is_free ? 'badge-free' : 'badge-premium'}">
                ${p.is_free ? '🎁 FREE' : '👑 PREMIUM'}
            </div>
            <img src="${p.image}" alt="${p.name}" class="product-img" onerror="this.src='assets/images/logo_ae.png'">
            <h3>${p.name}</h3>
            <p class="product-desc">${p.description}</p>
            <a href="${p.link}" class="btn-download ${p.is_free ? 'btn-free' : 'btn-premium'}">
                ${p.is_free ? '📥 Download' : '🔒 Get Access'}
            </a>
        </div>
    `).join('');
}