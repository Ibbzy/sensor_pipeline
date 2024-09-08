import React, { useState, createContext, useEffect } from 'react';
import axios from 'axios';

export const SensorModelContext = createContext();

export const SensorModelProvider = ({ children }) => {
    const [selectedSensor, setSelectedSensor] = useState('image');
    const [selectedModel, setSelectedModel] = useState('no model');
    const [models, setModels] = useState(['no model']);  // Default to 'none' initially

    const sensors = ['image', 'video', 'audio'];

    // Fetch models from the backend when the selectedSensor changes
    useEffect(() => {
        const fetchModels = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/models/`, {
                    params: { sensor_type: selectedSensor },
                });
                setModels(response.data.models);
            } catch (error) {
                console.error("Error fetching models: ", error);
            }
        };

        fetchModels();
    }, [selectedSensor]);

    return (
        <SensorModelContext.Provider
            value={{
                selectedSensor,
                setSelectedSensor,
                selectedModel,
                setSelectedModel,
                sensors,
                models,
            }}
        >
            {children}
        </SensorModelContext.Provider>
    );
};
