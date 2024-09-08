import React, { useState, useRef, useContext, useEffect } from 'react';
import { Button, CircularProgress, Typography, Stack } from '@mui/material';
import { SensorModelContext } from '../context/SensorModelContext';
import { uploadSensorData } from '../services/api';

const MediaCapture = ({ onUploadSuccess }) => {
    const { selectedSensor, selectedModel } = useContext(SensorModelContext);  // Get the selected sensor
    const [recording, setRecording] = useState(false);
    const [mediaStream, setMediaStream] = useState(null);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [chunks, setChunks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const videoRef = useRef(null);

    // Handle Start Capture
    const handleStartCapture = async () => {
        try {
            let stream;

            // Capture video, audio, or image stream
            if (selectedSensor === 'video' || selectedSensor === 'image') {
                stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: selectedSensor === 'video' });
            } else if (selectedSensor === 'audio') {
                stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            }

            // Set media stream for video or audio
            setMediaStream(stream);

            // If capturing video or image, assign stream to video element after rendering
            if (selectedSensor === 'video' || selectedSensor === 'audio') {
                const recorder = new MediaRecorder(stream);
                setMediaRecorder(recorder);

                recorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        setChunks((prev) => [...prev, event.data]);  // Collect recorded data
                    }
                };

                recorder.start();
                setRecording(true);  // Start recording
            } else if (selectedSensor === 'image') {
                const track = stream.getVideoTracks()[0];
                const imageCapture = new ImageCapture(track);
                const photoBlob = await imageCapture.takePhoto();
                handleUploadCapture(photoBlob, 'image');
            }
        } catch (error) {
            setMessage('Error accessing media devices: ' + error.message);
        }
    };

    // Assign mediaStream to videoRef after the video element is rendered
    useEffect(() => {
        if (videoRef.current && mediaStream && (selectedSensor === 'video' || selectedSensor === 'image')) {
            videoRef.current.srcObject = mediaStream;
        }
    }, [mediaStream, selectedSensor]);

    // Handle Stop Capture
    const handleStopCapture = () => {
        if (mediaRecorder) {
            mediaRecorder.stop();
        }
        if (mediaStream) {
            mediaStream.getTracks().forEach((track) => track.stop());
        }
        setRecording(false);  // Stop recording
    };

    // Handle Upload Capture
    const handleUploadCapture = async (blob, type = 'video') => {
        setLoading(true);
        const formData = new FormData();
        formData.append('file', blob, `capture.${type === 'image' ? 'jpg' : 'webm'}`);
        formData.append('sensor_type', selectedSensor);
        formData.append('model', selectedModel);

        uploadSensorData(formData)
            .then(response => {
                setLoading(false);
                setMessage('Capture uploaded successfully');
                onUploadSuccess(response.data.file_path);  // Assuming `file_path` is returned
            })
            .catch(error => {
                setLoading(false);
                setMessage('Error uploading capture: ' + error.message);
            });
    };

    return (
        <div style={{ marginTop: '20px' }}>
            {/* Show loading spinner while waiting for camera to initialize */}
            {loading && <CircularProgress size={24} />}
            
            <Stack spacing={2} alignItems="center">
                {/* Button to start/stop capture based on sensor type */}
                {!recording ? (
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={handleStartCapture}
                        disabled={loading}
                    >
                        Start {selectedSensor.charAt(0).toUpperCase() + selectedSensor.slice(1)} Capture
                    </Button>
                ) : (
                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={handleStopCapture}
                        disabled={loading}
                    >
                        Stop Capture
                    </Button>
                )}

                {/* Render video if sensor is video or image and stream is available */}
                {(selectedSensor === 'video' || selectedSensor === 'image') && mediaStream && (
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        style={{ width: '100%', maxWidth: '500px', borderRadius: '8px', marginBottom: '20px' }}
                    />
                )}

                {/* If media has been captured, allow upload */}
                {!recording && chunks.length > 0 && selectedSensor !== 'image' && (
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => handleUploadCapture(new Blob(chunks, { type: 'video/webm' }), selectedSensor)}
                        disabled={loading}
                    >
                        {loading ? <CircularProgress size={24} /> : `Upload ${selectedSensor} Capture`}
                    </Button>
                )}
            </Stack>

            {/* Display status message */}
            {message && (
                <Typography variant="body1" color="textSecondary" style={{ marginTop: '20px' }}>
                    {message}
                </Typography>
            )}
        </div>
    );
};

export default MediaCapture;
