const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1400,
        height: 900,
        webPreferences: {
            nodeIntegration: true,
        },
        title: "NEXUS SUPREME - COMMAND CENTER",
        backgroundColor: '#050a0f',
        icon: path.join(__dirname, '../assets/images/nexus_avatar.png')
    });

    // Load the supreme hub
    win.loadFile(path.join(__dirname, '../nexus_v2.html'));

    // win.webContents.openDevTools(); // Option for debugging
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
