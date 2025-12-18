// Netlify Serverless Function: Validate User Session
// This runs on Netlify's servers, NOT in the browser - so it's secure

exports.handler = async (event, context) => {
    // Get user from Netlify Identity context
    const { identity, user } = context.clientContext || {};

    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    };

    // Handle preflight
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    // No user = not logged in
    if (!user) {
        return {
            statusCode: 401,
            headers,
            body: JSON.stringify({
                authenticated: false,
                message: 'Not authenticated. Please log in.'
            })
        };
    }

    // User is authenticated - return secure data
    return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
            authenticated: true,
            user: {
                email: user.email,
                name: user.user_metadata?.full_name || user.email.split('@')[0],
                roles: user.app_metadata?.roles || ['user'],
                isPremium: user.app_metadata?.roles?.includes('premium') || false,
                isAdmin: user.app_metadata?.roles?.includes('admin') || false
            },
            // Secure server-validated data that can't be faked
            serverTime: new Date().toISOString(),
            validated: true
        })
    };
};
