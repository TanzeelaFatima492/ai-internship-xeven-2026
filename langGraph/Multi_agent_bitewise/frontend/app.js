// ==================== CONFIGURATION ====================
const API_BASE = "http://localhost";

const SERVICES = {
    patterns: `${API_BASE}:8001`,
    offers: `${API_BASE}:8002`,
    notifications: `${API_BASE}:8003`,
};

let currentUser = "user-001";

// ==================== UI HELPERS ====================

function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function setContent(containerId, html) {
    document.getElementById(containerId).innerHTML = html;
}

function showLoading(containerId) {
    setContent(containerId, "<p>⏳ Loading...</p>");
}

// ==================== USER FUNCTIONS ====================

function getUserId() {
    return document.getElementById("userId").value.trim() || "user-001";
}

async function seedUser() {
    const userId = getUserId();
    showToast(`🌱 Seeding data for ${userId}...`);
    
    try {
        const response = await fetch(`${SERVICES.patterns}/seed/${userId}`, {
            method: "POST",
        });
        const data = await response.json();
        showToast(`✅ ${data.message}`);
        await analyzeUser();
    } catch (error) {
        showToast(`❌ Error seeding: ${error.message}`);
    }
}

// ==================== PATTERN FUNCTIONS ====================

async function analyzeUser() {
    const userId = getUserId();
    currentUser = userId;
    showLoading("patterns-container");
    
    try {
        const response = await fetch(`${SERVICES.patterns}/user/${userId}/patterns`);
        const data = await response.json();
        
        if (data.status === "insufficient_data") {
            setContent("patterns-container", `
                <p>⚠️ ${data.message}</p>
                <button onclick="seedUser()">🌱 Seed Data</button>
            `);
            return;
        }
        
        renderPatterns(data);
        showToast(`✅ Patterns loaded for ${userId}`);
    } catch (error) {
        setContent("patterns-container", `<p>❌ Error: ${error.message}</p>`);
        showToast(`❌ Error: ${error.message}`);
    }
}

function renderPatterns(data) {
    const html = `
        <div class="pattern-item"><strong>📊 Total Orders:</strong> ${data.total_orders}</div>
        <div class="pattern-item"><strong>⏰ Routine:</strong> ${data.routine.routine} (${data.routine.confidence * 100}% confidence)</div>
        ${data.routine.usual_time ? `<div class="pattern-item"><strong>🕐 Usual Time:</strong> ${data.routine.usual_time}</div>` : ''}
        <div class="pattern-item"><strong>🔥 Streak:</strong> ${data.streak} days</div>
        <div class="pattern-item"><strong>💰 Spending:</strong> $${data.spending.average} avg | $${data.spending.total_spent} total</div>
        <div class="pattern-item"><strong>📈 Trend:</strong> ${data.spending.trend}</div>
        <div class="pattern-item"><strong>🍔 Favorites:</strong> ${data.preferences.favorites.map(f => f.name).join(', ')}</div>
        <div class="pattern-item"><strong>🏷️ Categories:</strong> ${data.preferences.categories.map(c => c.name).join(', ')}</div>
        ${data.preferences.combos.length ? `
            <div class="pattern-item"><strong>🍕 Combos:</strong> ${data.preferences.combos.map(c => c.items.join(' + ')).join(' | ')}</div>
        ` : ''}
        <div class="pattern-item"><strong>📅 Timing:</strong> ${data.timing_pattern.pattern} (${data.timing_pattern.confidence * 100}% confidence)</div>
        <div class="pattern-item"><strong>📆 Last Order:</strong> ${new Date(data.last_order).toLocaleString()}</div>
    `;
    setContent("patterns-container", html);
}

// ==================== OFFER FUNCTIONS ====================

async function generateOffers() {
    const userId = getUserId();
    showLoading("offers-container");
    
    try {
        const response = await fetch(`${SERVICES.offers}/offers/generate/${userId}`, {
            method: "POST",
        });
        const data = await response.json();
        
        if (data.status === "insufficient_data") {
            setContent("offers-container", `<p>⚠️ ${data.message}</p>`);
            return;
        }
        
        renderOffers(data);
        showToast(`🎁 ${data.total_offers} offers generated!`);
        
        // Refresh notifications
        getNotifications();
    } catch (error) {
        setContent("offers-container", `<p>❌ Error: ${error.message}</p>`);
        showToast(`❌ Error: ${error.message}`);
    }
}

function renderOffers(data) {
    if (data.offers.length === 0) {
        setContent("offers-container", "<p>😴 No offers generated</p>");
        return;
    }
    
    const html = data.offers.map(offer => `
        <div class="offer-item ${offer.priority}">
            <strong>${offer.message}</strong>
            ${offer.discount ? `<span class="discount">${offer.discount}</span>` : ''}
            <div style="font-size:0.8rem;color:#999;margin-top:4px;">
                ${offer.priority.toUpperCase()} Priority
                ${offer.type ? `| ${offer.type.replace('_', ' ')}` : ''}
            </div>
        </div>
    `).join('');
    
    setContent("offers-container", html);
}

// ==================== NOTIFICATION FUNCTIONS ====================

async function getNotifications() {
    const userId = getUserId();
    showLoading("notifications-container");
    
    try {
        const response = await fetch(`${SERVICES.notifications}/notifications/${userId}?limit=20`);
        const data = await response.json();
        renderNotifications(data);
    } catch (error) {
        setContent("notifications-container", `<p>❌ Error: ${error.message}</p>`);
        showToast(`❌ Error: ${error.message}`);
    }
}

function renderNotifications(data) {
    if (data.notifications.length === 0) {
        setContent("notifications-container", "<p>📭 No notifications</p>");
        return;
    }
    
    const html = data.notifications.map(notif => `
        <div class="notification-item ${notif.read ? '' : 'unread'}">
            <span>${notif.icon || '📌'} ${notif.message}</span>
            <div>
                <span class="time">${new Date(notif.created_at).toLocaleString()}</span>
                ${!notif.read ? `<button onclick="markRead('${notif.id}')" style="margin-left:10px;background:#e17055;color:white;padding:2px 8px;border:none;border-radius:4px;">Mark Read</button>` : ''}
            </div>
        </div>
    `).join('');
    
    setContent("notifications-container", html);
}

async function markRead(notificationId) {
    const userId = getUserId();
    try {
        await fetch(`${SERVICES.notifications}/notifications/${userId}/${notificationId}/read`, {
            method: "PUT",
        });
        getNotifications();
        showToast("✅ Marked as read");
    } catch (error) {
        showToast(`❌ Error: ${error.message}`);
    }
}

async function markAllRead() {
    const userId = getUserId();
    try {
        await fetch(`${SERVICES.notifications}/notifications/${userId}/read-all`, {
            method: "PUT",
        });
        getNotifications();
        showToast("✅ All notifications marked as read");
    } catch (error) {
        showToast(`❌ Error: ${error.message}`);
    }
}

// ==================== WEBSOCKET (Real-time) ====================

let ws = null;

function connectWebSocket() {
    const userId = getUserId();
    const wsUrl = `ws://localhost:8003/ws/${userId}`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        console.log("🔌 WebSocket connected");
    };
    
    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.type === "new_notification") {
                const notif = data.data;
                showToast(`🔔 ${notif.message}`);
                getNotifications();
            }
        } catch (e) {
            console.error("WebSocket error:", e);
        }
    };
    
    ws.onclose = () => {
        console.log("🔌 WebSocket disconnected, reconnecting...");
        setTimeout(connectWebSocket, 3000);
    };
    
    ws.onerror = (error) => {
        console.error("WebSocket error:", error);
    };
}

// ==================== AUTO-LOAD ====================

// Load patterns when page loads
window.onload = function() {
    analyzeUser();
    connectWebSocket();
    
    // Auto-refresh notifications every 30 seconds
    setInterval(() => {
        getNotifications();
    }, 30000);
};


// ==================== CONFIGURATION ====================
const API_BASE = "http://localhost";
const SERVICES = {
    patterns: `${API_BASE}:8001`,
    offers: `${API_BASE}:8002`,
    notifications: `${API_BASE}:8003`,
};

let currentUser = "user-001";

// ==================== USER FUNCTIONS ====================

async function createUser() {
    const name = document.getElementById("userName").value;
    const email = document.getElementById("userEmail").value;
    const phone = document.getElementById("userPhone").value;
    
    if (!name || !email) {
        showToast("❌ Name and email are required");
        return;
    }
    
    try {
        const response = await fetch(
            `${SERVICES.patterns}/user?name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&phone=${encodeURIComponent(phone || '')}`,
            { method: "POST" }
        );
        const data = await response.json();
        if (response.ok) {
            showToast(`✅ User created: ${data.user_id}`);
            document.getElementById("userId").value = data.user_id;
            currentUser = data.user_id;
            analyzeUser();
        } else {
            showToast(`❌ ${data.detail}`);
        }
    } catch (error) {
        showToast(`❌ Error: ${error.message}`);
    }
}

function getUserId() {
    return document.getElementById("userId").value.trim() || "user-001";
}

// Update HTML to include user creation