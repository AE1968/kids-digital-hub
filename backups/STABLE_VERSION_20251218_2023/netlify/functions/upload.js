// Netlify Serverless Function: Image Upload Handler
// Uses Cloudinary for free cloud storage (10GB free)

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
            body: JSON.stringify({ error: 'Not authenticated. Please log in.' })
        };
    }

    if (event.httpMethod === 'POST') {
        try {
            const body = JSON.parse(event.body || '{}');
            const { image, filename, category } = body;

            if (!image) {
                return {
                    statusCode: 400,
                    headers,
                    body: JSON.stringify({ error: 'No image data provided' })
                };
            }

            // Cloudinary upload (requires env vars: CLOUDINARY_URL)
            const cloudinaryUrl = process.env.CLOUDINARY_URL;

            if (!cloudinaryUrl) {
                // Fallback: Return success but note that cloud storage isn't configured
                console.log('Cloudinary not configured, simulating upload');
                return {
                    statusCode: 200,
                    headers,
                    body: JSON.stringify({
                        success: true,
                        message: 'Upload simulated (Cloudinary not configured)',
                        simulated: true,
                        filename: filename || 'upload.png',
                        userId: user.sub,
                        timestamp: new Date().toISOString()
                    })
                };
            }

            // Parse Cloudinary URL
            // Format: cloudinary://API_KEY:API_SECRET@CLOUD_NAME
            const cloudinaryParts = cloudinaryUrl.replace('cloudinary://', '').split('@');
            const [apiKey, apiSecret] = cloudinaryParts[0].split(':');
            const cloudName = cloudinaryParts[1];

            // Build upload URL
            const uploadUrl = `https://api.cloudinary.com/v1_1/${cloudName}/image/upload`;

            // Upload to Cloudinary
            const formData = new FormData();
            formData.append('file', image);
            formData.append('upload_preset', 'kids_hub_unsigned'); // Configure in Cloudinary dashboard
            formData.append('folder', `kids-hub/${user.sub}/${category || 'general'}`);

            const response = await fetch(uploadUrl, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                return {
                    statusCode: 200,
                    headers,
                    body: JSON.stringify({
                        success: true,
                        url: result.secure_url,
                        publicId: result.public_id,
                        width: result.width,
                        height: result.height
                    })
                };
            } else {
                const error = await response.text();
                return {
                    statusCode: 500,
                    headers,
                    body: JSON.stringify({ error: 'Upload failed', details: error })
                };
            }

        } catch (error) {
            console.error('Upload error:', error);
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({ error: 'Upload failed', message: error.message })
            };
        }
    }

    // GET: List user's uploads
    if (event.httpMethod === 'GET') {
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                message: 'Upload endpoint ready',
                userId: user.sub,
                storageUsed: '0 MB', // In production: calculate from DB
                storageLimit: user.app_metadata?.roles?.includes('premium') ? 'Unlimited' : '100 MB'
            })
        };
    }

    return {
        statusCode: 405,
        headers,
        body: JSON.stringify({ error: 'Method not allowed' })
    };
};
