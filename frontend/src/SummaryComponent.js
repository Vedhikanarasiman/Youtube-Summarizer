import React, { useState } from 'react';
import axios from 'axios';

const SummaryComponent = () => {
    const [youtubeLink, setYoutubeLink] = useState('');
    const [summary, setSummary] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleInputChange = (event) => {
        setYoutubeLink(event.target.value);
    };

    const extractVideoId = (url) => {
        const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        const match = url.match(regExp);
        return (match && match[2].length === 11) ? match[2] : null;
    };

    const fetchSummary = async () => {
        setIsLoading(true);
        setError('');
        setSummary('');
        try {
            const videoId = extractVideoId(youtubeLink);
            if (!videoId) {
                setError('Invalid YouTube URL');
                return;
            }
            const response = await axios.get(`http://localhost:8000/summary?video_id=${videoId}`);
            const { summary } = response.data;
            setSummary(summary);
        } catch (error) {
            console.error('Error fetching summary:', error);
            setError('Failed to fetch summary. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ textAlign: 'center', maxWidth: '600px', margin: 'auto', padding: '20px' }}>
            <h1 style={{ marginBottom: '20px' }}>YouTube Video Summary</h1>
            <input
                type="text"
                value={youtubeLink}
                onChange={handleInputChange}
                placeholder="Enter YouTube Video Link"
                style={{ width: '80%', padding: '10px', marginBottom: '20px', fontSize: '16px' }}
            />
            <br />
            <button 
                onClick={fetchSummary} 
                style={{ 
                    padding: '10px 20px', 
                    fontSize: '16px',
                    backgroundColor: isLoading ? '#cccccc' : '#4CAF50',
                    color: 'white',
                    border: 'none',
                    cursor: isLoading ? 'not-allowed' : 'pointer'
                }} 
                disabled={isLoading}
            >
                {isLoading ? 'Loading...' : 'Get Summary'}
            </button>
            <br />
            {error && <p style={{ color: 'red', marginTop: '20px' }}>{error}</p>}
            {summary && (
                <div style={{ marginTop: '30px', textAlign: 'left' }}>
                    <h2>Summary:</h2>
                    <p style={{ whiteSpace: 'pre-wrap' }}>{summary}</p>
                </div>
            )}
        </div>
    );
};

export default SummaryComponent;