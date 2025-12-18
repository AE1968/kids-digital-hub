// THIS IS A SERVERLESS FUNCTION
// It runs on Netlify's backend infrastructure, not in the browser.
// Use this to handle secure things like Database updates, Payment Webhooks, etc.

const handler = async (event, context) => {
    // 1. Validate the Request (Ensure it comes from PayPal/Stripe)
    if (event.httpMethod !== "POST") {
        return { statusCode: 405, body: "Method Not Allowed" };
    }

    try {
        const payload = JSON.parse(event.body);
        console.log("💰 Payment Webhook Received:", payload);

        // 2. Extract User Info & Plan
        // (In a real scenario, PayPal sends 'custom' field with user ID)
        const userId = payload.custom_id || "unknown_user";
        const plan = payload.item_name || "monthly_hero";

        // 3. Connect to "Database" (Netlify Identity in this case)
        // We would use the Netlify Identity Admin API here to update the user's roles
        // const identity = context.clientContext.identity;
        // await updateUserRole(identity, userId, 'premium');

        return {
            statusCode: 200,
            body: JSON.stringify({ message: "Webhook Processed", status: "premium_active" }),
        };
    } catch (error) {
        return { statusCode: 400, body: JSON.stringify({ message: "Invalid Payload" }) };
    }
};

exports.handler = handler;
