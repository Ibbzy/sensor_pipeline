import React, { useContext } from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { SensorModelContext } from '../context/SensorModelContext';

const SensorSelector = () => {
    const { sensors, selectedSensor, setSelectedSensor } = useContext(SensorModelContext);

    return (
        <FormControl style={{ maxWidth: 600, minWidth: 400, textAlign: 'center'  }} variant="outlined" margin="normal">
            <InputLabel id="sensor-selector-label">Select Sensor</InputLabel>
            <Select
                labelId="sensor-selector-label"
                value={selectedSensor}
                onChange={(e) => setSelectedSensor(e.target.value)}
                label="Select Sensor"
            >
                {sensors.map((sensor, index) => (
                    <MenuItem key={index} value={sensor}>
                        {sensor}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
};

export default SensorSelector;
