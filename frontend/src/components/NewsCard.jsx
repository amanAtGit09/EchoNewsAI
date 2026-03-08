// This component is not being used in the current version of the app.

import React from 'react';
import { Play, ExternalLink } from 'lucide-react';

const NewsCard = ({ news, onPlay }) => {
  // Use a generic news image if the article doesn't provide one
  const image = news.image || "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&q=80&w=300";

  return (
    <div className="news-card">
      <div style={{ position: 'relative' }}>
        <img src={image} alt={news.title} style={{ width: '100%', height: '160px', objectFit: 'cover' }} />
        <button 
          onClick={() => onPlay(news.audio_url)}
          className="play-overlay-btn"
        >
          <Play fill="white" size={24} />
        </button>
      </div>
      
      <div style={{ padding: '12px' }}>
        <p style={{ fontSize: '10px', color: '#00d4ff', textTransform: 'uppercase', marginBottom: '4px' }}>
          {news.source_id || "Global News"}
        </p>
        <h3 style={{ fontSize: '14px', margin: '0 0 8px 0', height: '40px', overflow: 'hidden' }}>
          {news.title}
        </h3>
        <a href={news.link} target="_blank" rel="noreferrer" style={{ color: '#888', fontSize: '12px', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px' }}>
          Read Article <ExternalLink size={12} />
        </a>
      </div>
    </div>
  );
};

export default NewsCard;