import React, { useContext } from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { SensorModelContext } from '../context/SensorModelContext';

const ModelSelector = () => {
    const { models, selectedModel, setSelectedModel } = useContext(SensorModelContext);

    return (
        <FormControl style={{ maxWidth: 600, minWidth: 400, textAlign: 'center' }} variant="outlined" margin="normal">
            <InputLabel id="model-selector-label">Select Model</InputLabel>
            <Select
                labelId="model-selector-label"
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                label="Select Model"
            >
                {models.map((model, index) => (
                    <MenuItem key={index} value={model}>
                        {model}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
};

export default ModelSelector;
