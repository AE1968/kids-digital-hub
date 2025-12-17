
class AuthManager {
    constructor() {
        this.currentUser = JSON.parse(localStorage.getItem('kdh_user')) || null;
        this.users = {
            'admin': { pass: 'admin123', role: 'admin', storage: 'Unlimited' },
            'user1': { pass: 'pass1', role: 'premium_low', storage: '500GB' }, // £2
            'user2': { pass: 'pass2', role: 'premium_mid', storage: '2TB' },   // £4
            'user3': { pass: 'pass3', role: 'premium_high', storage: '10TB' }, // £10
            'demo': { pass: 'demo', role: 'free', storage: '100MB' }
        };
    }

    login(username, password) {
        const user = this.users[username];
        if (user && user.pass === password) {
            this.currentUser = { username, role: user.role, storage: user.storage };
            localStorage.setItem('kdh_user', JSON.stringify(this.currentUser));
            window.location.reload();
            return true;
        }
        return false;
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('kdh_user');
        window.location.reload();
    }

    isLoggedIn() {
        return !!this.currentUser;
    }

    isAdmin() {
        return this.currentUser && this.currentUser.role === 'admin';
    }

    getStorageLimit() {
        return this.currentUser ? this.currentUser.storage : '0GB';
    }

    // Apply protection rules to the current page
    applyProtection() {
        // Rule: Guests don't see Premium folder
        // Rule: Logged in users see Premium folder but read-only (unless admin)

        const premiumSlots = document.querySelectorAll('.slot .empty-label span');
        const premiumContainers = [];

        // Find containers marked as Premium (based on the text "Premium" or specific class if added)
        // Currently relying on text content in the gallery HTMLs: "🔒 Premium"

        document.querySelectorAll('.slot').forEach(slot => {
            if (slot.innerText.includes('Premium')) {
                premiumContainers.push(slot);
            }
        });

        if (!this.isLoggedIn()) {
            // Guest: Hide Premium Directory or Lock it harder
            premiumContainers.forEach(slot => {
                slot.style.opacity = '0.5';
                slot.style.pointerEvents = 'none';
                slot.title = "Login required";
                // Optionally hide it completely via CSS class
                // slot.style.display = 'none'; // User said "nu vor vedea" (won't see)
                slot.style.display = 'none';
            });
        } else {
            // Logged In: Show it (View Only is default for slots unless they have delete buttons)
            premiumContainers.forEach(slot => {
                slot.style.display = 'flex';
                slot.style.opacity = '1';
                slot.style.pointerEvents = 'auto'; // But maybe just for viewing
            });
        }

        // Admin checks for Delete buttons
        const deleteBtns = document.querySelectorAll('.btn-delete');
        deleteBtns.forEach(btn => {
            if (!this.isAdmin()) {
                btn.style.display = 'none'; // Only admin can delete/modify
            } else {
                btn.style.display = 'flex';
            }
        });
    }
}

const auth = new AuthManager();

document.addEventListener('DOMContentLoaded', () => {
    auth.applyProtection();

    // Setup login form if on dashboard
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        if (auth.isLoggedIn()) {
            document.getElementById('login-section').style.display = 'none';
            document.getElementById('profile-section').style.display = 'block';
            document.getElementById('user-name-display').textContent = auth.currentUser.username;
            document.getElementById('storage-display').textContent = auth.currentUser.storage;
        } else {
            document.getElementById('login-section').style.display = 'block';
            document.getElementById('profile-section').style.display = 'none';
        }

        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const u = document.getElementById('username').value;
            const p = document.getElementById('password').value;
            if (!auth.login(u, p)) {
                alert('Invalid credentials!');
            }
        });
    }

    // Logout button
    const logoutBtn = document.getElementById('btn-logout');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => auth.logout());
    }
});
