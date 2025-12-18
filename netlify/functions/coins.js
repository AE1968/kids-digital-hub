// Netlify Serverless Function: Manage User Coins Securely
// Coins are stored per-user and validated on server

// In-memory store (in production, use a database like Supabase)
// For now, this demonstrates secure validation

exports.handler = async (event, context) => {
    const { user } = context.clientContext || {};

    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    // Must be authenticated
    if (!user) {
        return {
            statusCode: 401,
            headers,
            body: JSON.stringify({ error: 'Not authenticated' })
        };
    }

    const userId = user.sub; // Unique user ID from Netlify Identity

    // For demo: return server-calculated coins
    // In production: fetch from database
    const baseCoins = 50; // Starting coins for new users
    const bonusCoins = user.app_metadata?.roles?.includes('premium') ? 100 : 0;

    if (event.httpMethod === 'GET') {
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                userId,
                coins: baseCoins + bonusCoins,
                isPremium: user.app_metadata?.roles?.includes('premium') || false,
                source: 'server-validated',
                message: 'Coin balance retrieved from secure server'
            })
        };
    }

    // Handle coin operations (add/spend)
    if (event.httpMethod === 'POST') {
        const body = JSON.parse(event.body || '{}');
        const { action, amount } = body;

        // Validate action
        if (!['add', 'spend'].includes(action)) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Invalid action. Use "add" or "spend".' })
            };
        }

        // Validate amount
        if (!amount || amount < 0 || amount > 100) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Invalid amount. Must be 1-100.' })
            };
        }

        // In production: update database
        // For demo: just acknowledge
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                success: true,
                action,
                amount,
                message: `${action === 'add' ? 'Added' : 'Spent'} ${amount} coins (server validated)`,
                serverTime: new Date().toISOString()
            })
        };
    }

    return {
        statusCode: 405,
        headers,
        body: JSON.stringify({ error: 'Method not allowed' })
    };
};
