const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        title: "Nexus Supreme - Kids Digital Hub",
        icon: path.join(__dirname, 'assets/images/logo_ae.png'),
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        backgroundColor: '#0a0a12' // Dark background for Nexus Supreme
    });

    // Load the remote or local index
    // For production, we would use the Netlify URL
    win.loadURL('https://kidsdigitalhub.com');

    // Remove menu for premium feel
    Menu.setApplicationMenu(null);
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
