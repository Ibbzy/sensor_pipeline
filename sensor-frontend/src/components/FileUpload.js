import React, { useState, useContext } from 'react';
import { Button, CircularProgress, Typography } from '@mui/material';
import { SensorModelContext } from '../context/SensorModelContext';
import { uploadSensorData } from '../services/api';

const FileUpload = ({ onUploadSuccess }) => {
    const { selectedSensor, selectedModel } = useContext(SensorModelContext);
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = () => {
        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        formData.append('sensor_type', selectedSensor);
        formData.append('model', selectedModel);  // Assuming backend support for different models

        uploadSensorData(formData)
            .then(response => {
                setLoading(false);
                setMessage('File uploaded successfully');
                onUploadSuccess(response.data.urls);
            })
            .catch(error => {
                setLoading(false);
                setMessage(`Error uploading file: ${error.message}`);
            });
    };

    return (
        <div style={{ marginTop: '20px' }}>
            <input
                type="file"
                onChange={handleFileChange}
                style={{ marginBottom: '20px' }}
            />
            <Button
                variant="contained"
                color="primary"
                onClick={handleUpload}
                disabled={!file || loading}
            >
                {loading ? <CircularProgress size={24} /> : `Upload ${selectedSensor}`}
            </Button>
            {message && (
                <Typography variant="body1" color="textSecondary" style={{ marginTop: '20px' }}>
                    {message}
                </Typography>
            )}
        </div>
    );
};

export default FileUpload;
