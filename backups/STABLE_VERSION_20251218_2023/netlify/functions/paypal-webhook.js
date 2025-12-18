// Netlify Serverless Function: PayPal Webhook Handler
// Receives payment confirmations from PayPal and activates premium

const crypto = require('crypto');

exports.handler = async (event, context) => {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    };

    // Only accept POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const payload = JSON.parse(event.body);

        // Log webhook for debugging
        console.log('PayPal Webhook received:', {
            event_type: payload.event_type,
            resource_type: payload.resource_type,
            create_time: payload.create_time
        });

        // Check event type
        const eventType = payload.event_type;

        // Payment completed events
        if (eventType === 'PAYMENT.CAPTURE.COMPLETED' ||
            eventType === 'CHECKOUT.ORDER.APPROVED' ||
            eventType === 'PAYMENT.SALE.COMPLETED') {

            const resource = payload.resource;

            // Extract payment details
            const paymentInfo = {
                paymentId: resource.id,
                status: resource.status,
                amount: resource.amount?.value || resource.purchase_units?.[0]?.amount?.value,
                currency: resource.amount?.currency_code || 'GBP',
                email: resource.payer?.email_address || 'unknown',
                name: resource.payer?.name?.given_name || 'Customer',
                timestamp: new Date().toISOString()
            };

            console.log('Payment confirmed:', paymentInfo);

            // In production: Save to database (Supabase, Firebase, etc.)
            // For now: Log and acknowledge

            // TODO: Send email notification to Adrian
            // TODO: Update user role in Netlify Identity

            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    success: true,
                    message: 'Payment webhook processed successfully',
                    payment: paymentInfo
                })
            };
        }

        // Subscription events
        if (eventType === 'BILLING.SUBSCRIPTION.ACTIVATED') {
            console.log('Subscription activated:', payload.resource.id);

            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    success: true,
                    message: 'Subscription activation recorded'
                })
            };
        }

        // Subscription cancelled
        if (eventType === 'BILLING.SUBSCRIPTION.CANCELLED') {
            console.log('Subscription cancelled:', payload.resource.id);

            // TODO: Revoke premium access

            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    success: true,
                    message: 'Subscription cancellation recorded'
                })
            };
        }

        // Unknown event - acknowledge anyway
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                success: true,
                message: 'Webhook received (event type not handled)',
                event_type: eventType
            })
        };

    } catch (error) {
        console.error('Webhook processing error:', error);

        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Webhook processing failed',
                message: error.message
            })
        };
    }
};
