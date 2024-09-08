import React from 'react';
import FileUpload from './components/FileUpload';

function App() {
    return (
        <div className="App">
            <h1>Sensor Data Upload</h1>
            <FileUpload sensorType="image" />
            <FileUpload sensorType="audio" />
            <FileUpload sensorType="video" />
        </div>
    );
}

export default App;
