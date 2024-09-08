import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import SensorSelector from './components/SensorSelector';
import ModelSelector from './components/ModelSelector';
import DataVisualization from './components/DataVisualization';
import { SensorModelProvider } from './context/SensorModelContext';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import './styles/App.css';
import rikaiLogo from './assets/rikai-logo-black.png';

function App() {
    const [fileUrls, setFileUrls] = useState([]);

    const handleUploadSuccess = (urls) => {
        setFileUrls(urls);
    };

    return (
        <SensorModelProvider>
            <div className="App">
                {/* Navbar */}
                <AppBar position="static" style={{ backgroundColor: '#0066CC' }}>
                    <Toolbar>
                        <Typography variant="h6" style={{ flexGrow: 1 }}>
                            Rikai Labs
                        </Typography>
                        <Button color="inherit">Models</Button>
                        <Button color="inherit">Documentation</Button>
                    </Toolbar>
                </AppBar>
                {/* Main content */}
                <Box className="main-content">
                    {/* Large title or logo */}
                    <img
                        src={rikaiLogo}  // Placeholder image, replace with your logo URL
                        //src="https://www.trustedreviews.com/wp-content/uploads/sites/54/2023/05/Copy-of-Logitech-G-Cloud-vs-Razer-Edge-5G.jpg"
                        alt="Rikai Labs Logo"
                        className="logo"
                    />
                    <div className="selector-container">
                        <SensorSelector />
                        <ModelSelector />
                    </div>
                    <FileUpload onUploadSuccess={handleUploadSuccess} />
                    {fileUrls.length > 0 && <DataVisualization fileUrls={fileUrls} />}
                </Box>
            </div>
        </SensorModelProvider>
    );
}

export default App;
