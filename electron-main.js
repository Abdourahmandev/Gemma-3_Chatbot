const { app, BrowserWindow, shell } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let streamlitProcess = null;
let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    },
    icon: path.join(__dirname, 'icon.ico'),
    title: 'Gemma 3 ChatBot'
  });

  // Start Streamlit process
  startStreamlit();
  
  // Load the Streamlit URL after a delay
  setTimeout(() => {
    mainWindow.loadURL('http://localhost:8501');
  }, 3000);

  // Open external links in browser
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

function startStreamlit() {
  const pythonPath = path.join(__dirname, 'venv', 'Scripts', 'python.exe');
  const appPath = path.join(__dirname, 'app.py');
  
  streamlitProcess = spawn(pythonPath, ['-m', 'streamlit', 'run', appPath, '--server.port', '8501', '--server.headless', 'true'], {
    cwd: __dirname
  });

  streamlitProcess.on('error', (err) => {
    console.error('Failed to start Streamlit:', err);
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (streamlitProcess) {
    streamlitProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
