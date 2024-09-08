import React from 'react';
import { Grid, Typography, Card, CardMedia } from '@mui/material';

const DataVisualization = ({ fileUrls }) => {
    return (
        <div style={{ marginTop: '30px' }}>
            <Typography variant="h5" gutterBottom>
                Data Visualization
            </Typography>
            <Grid container spacing={3}>
                {fileUrls.map((url, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                        <Card>
                            <CardMedia
                                component="img"
                                alt={`Processed Frame ${index}`}
                                image={url}
                                title={`Processed Frame ${index}`}
                            />
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </div>
    );
};

export default DataVisualization;
