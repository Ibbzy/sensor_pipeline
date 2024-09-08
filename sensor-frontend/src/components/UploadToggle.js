import React from 'react';
import { FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material';

const UploadToggle = ({ mode, setMode }) => {
    return (
        <FormControl component="fieldset" style={{ marginBottom: '20px' }}>
            <FormLabel component="legend">Choose Upload Method</FormLabel>
            <RadioGroup row value={mode} onChange={(e) => setMode(e.target.value)}>
                <FormControlLabel value="file" control={<Radio />} label="File Upload" />
                <FormControlLabel value="capture" control={<Radio />} label="Media Capture" />
            </RadioGroup>
        </FormControl>
    );
};

export default UploadToggle;
