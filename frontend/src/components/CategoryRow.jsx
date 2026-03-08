import React, { useState, useEffect } from 'react';
import DigestCard from './DigestCard';
import { fetchNews } from '../api';
import { RefreshCw, Zap, AlertCircle } from 'lucide-react';
import NewsModal from './NewsModal';  

const CategoryRow = ({ title, category, isBriefing = false, initialData = null, isSearch = false, onPlay, currentAudio, onOpenDetail}) => {
  const [digests, setDigests] = useState(initialData || []);
  const [loading, setLoading] = useState(!initialData);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isSearch && initialData) {
      setDigests(initialData);
      setLoading(false);
    }
  }, [initialData, isSearch]);
  
  // Load Historical Data from DB on mount
  useEffect(() => {
    if (initialData) return; // Skip if this is a Search row with data already provided

    const loadHistory = async () => {
      setLoading(true);
      setError(null);

      const data = await fetchNews({ 
        type: isBriefing? 'briefing' : 'history', 
        category: category 
      });

      if (data && Array.isArray(data)) {
        setDigests(data);
       // console.log(data);
      } else if (data && data.BriefingID) {
        // If backend returns a single object instead of an array
        setDigests([data]);
      }
      setLoading(false);
    };

    loadHistory();
  }, [category, initialData]);

  // Handle the "AI Refresh" (Pipeline)
  const handleRefresh = async () => {
    setLoading(true);
    setError(null)
    const newData = await fetchNews({ type: 'pipeline', category });
    
    if (newData && newData.BriefingID) {
      setDigests(prev => [newData, ...prev]);
    } else {
      setError("Failed to generate latest news. Try again later.");
    }
    setLoading(false);
  };

  return (
    <div className="row-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 'bold', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
          {title} {title === "Trending Now" && <span className="live-dot" />}
        </h2>
        
        {!isSearch && (
          <button onClick={handleRefresh} disabled={loading} className="refresh-btn">
            {loading ? <RefreshCw className="spin" size={14} /> : <Zap size={14} />}
            {loading ? "Generating..." : "Get Latest"}
          </button>
        )}
      </div>

      {error && <div className="error-msg"><AlertCircle size={14}/> {error}</div>}

      <div className="horizontal-scroll">
        {loading && digests.length === 0 ? (
          // Skeleton loaders
          [1, 2, 3].map(i => <div key={i} className="skeleton-card" style={{ minWidth: '320px' }} />)
        ) : (
          digests.map((digest, index) => (
            <DigestCard 
              key={digest.BriefingID || `search-result-${index}`} 
              digest={digest} 
              onPlay={onPlay}
              isPlaying={currentAudio === digest.audio_url}
              onOpenDetail={onOpenDetail}
            />
          ))
        )}
        
        {!loading && digests.length === 0 && !error && (
          <p style={{ color: '#555', fontSize: '14px', padding: '20px' }}>No stories found in the vault.</p>
        )}
      </div>
    </div>
  );
};

export default CategoryRow;