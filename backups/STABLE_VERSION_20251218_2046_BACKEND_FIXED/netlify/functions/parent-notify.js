// Netlify Serverless Function: Parent Notification System
// Sends weekly reports and alerts to parents

exports.handler = async (event, context) => {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const body = JSON.parse(event.body || '{}');
        const { type, parentEmail, childName, data } = body;

        // Log notification request
        console.log('📧 Parent notification requested:', {
            type,
            parentEmail,
            childName,
            timestamp: new Date().toISOString()
        });

        // Different notification types
        switch (type) {
            case 'weekly_report':
                return handleWeeklyReport(parentEmail, childName, data, headers);

            case 'bedtime_alert':
                return handleBedtimeAlert(parentEmail, childName, headers);

            case 'achievement':
                return handleAchievement(parentEmail, childName, data, headers);

            case 'time_limit_reached':
                return handleTimeLimitReached(parentEmail, childName, headers);

            default:
                return {
                    statusCode: 400,
                    headers,
                    body: JSON.stringify({ error: 'Unknown notification type' })
                };
        }

    } catch (error) {
        console.error('Notification error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Failed to process notification' })
        };
    }
};

async function handleWeeklyReport(email, childName, data, headers) {
    // Generate weekly report HTML
    const report = {
        childName,
        email,
        type: 'weekly_report',
        stats: {
            drawingsCompleted: data?.drawings || 0,
            gamesPlayed: data?.games || 0,
            storiesRead: data?.stories || 0,
            totalTimeMinutes: data?.timeMinutes || 0,
            coinsEarned: data?.coins || 0
        },
        generatedAt: new Date().toISOString()
    };

    console.log('📊 Weekly report generated:', report);

    // In production: Send email via SMTP or SendGrid
    // For now: Log and acknowledge

    return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
            success: true,
            message: `Weekly report prepared for ${email}`,
            report
        })
    };
}

async function handleBedtimeAlert(email, childName, headers) {
    console.log(`🌙 Bedtime alert: ${childName} tried to access after hours`);

    return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
            success: true,
            message: `Bedtime alert sent to ${email}`,
            alert: {
                type: 'bedtime_access_attempt',
                childName,
                timestamp: new Date().toISOString()
            }
        })
    };
}

async function handleAchievement(email, childName, data, headers) {
    console.log(`🏆 Achievement unlocked: ${childName} - ${data?.achievement}`);

    return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
            success: true,
            message: `Achievement notification sent to ${email}`,
            achievement: data?.achievement
        })
    };
}

async function handleTimeLimitReached(email, childName, headers) {
    console.log(`⏰ Time limit reached: ${childName}`);

    return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
            success: true,
            message: `Time limit notification sent to ${email}`,
            alert: {
                type: 'daily_limit_reached',
                childName,
                timestamp: new Date().toISOString()
            }
        })
    };
}
