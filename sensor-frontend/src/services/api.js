import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const uploadSensorData = (data) => {
    return axios.post(`${API_URL}/upload/`, data, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};
