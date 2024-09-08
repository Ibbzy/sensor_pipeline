import React, { useState } from 'react';
import { uploadSensorData } from '../services/api';

const FileUpload = ({ sensorType }) => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = () => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('sensor_type', sensorType);

        uploadSensorData(formData)
            .then(response => {
                setMessage(`File uploaded successfully: ${response.data.url}`);
            })
            .catch(error => {
                setMessage(`Error uploading file: ${error.message}`);
            });
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload {sensorType}</button>
            <p>{message}</p>
        </div>
    );
};

export default FileUpload;
