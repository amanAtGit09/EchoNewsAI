import React from 'react';
import { Play, Pause, History, ChevronRight, Info } from 'lucide-react';

const DigestCard = ({ digest, onPlay, isPlaying, onOpenDetail }) => {
  // Safe Extraction: Detect if digest is an array (search result)
  const data = Array.isArray(digest) ? digest[0] : digest;

  const headlines = data.Headlines || [];
  
  // Label Logic: Parse specific tags from BriefingID
  const label = data.BriefingID?.includes('MORNING') ? 'MORNING' 
              : data.BriefingID?.includes('AFTERNOON') ? 'AFTERNOON'
              : data.BriefingID?.includes('EVENING') ? 'EVENING'
              : data.BriefingID?.includes('TECHNOLOGY') ? 'TECHNOLOGY'
              : data.BriefingID?.includes('BUSINESS') ? 'BUSINESS'
              : data.BriefingID?.includes('SPORTS') ? 'SPORTS'
              : data.BriefingID?.includes('ENTERTAINMENT') ? 'ENTERTAINMENT'
              : data.BriefingID?.includes('POLITICS') ? 'POLITICS'
              : 'SEARCH';

  // Date & Time Logic (Fixed initialization order)
  const timestamp = typeof data.CreatedAt === 'number' 
    ? data.CreatedAt * 1000 
    : Date.parse(data.CreatedAt);

  const formattedDate = !isNaN(timestamp)
    ? new Date(timestamp).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })
    : "Recently";

  // Past News Logic (Using the safe timestamp)
  const isPastNews = !isNaN(timestamp) 
    ? new Date(timestamp) < new Date(Date.now() - 3600000)
    : false;

  
  // Collage Logic: Get top 3 images
  const images = headlines.filter(h => h.image).map(h => h.image).slice(0, 3);

  // Play/Pause Toggle Logic
  const handlePlayClick = () => {
    if (isPlaying) {
      onPlay(null);
    } else {
      onPlay(data.audio_url);
    }
  };

  return (
    <div className={`digest-card ${isPastNews ? 'historical' : 'latest'}`}>
      <div className="collage-container">
        {/* Collage Grid */}
        <div className={`collage-grid images-${images.length}`}>
          {images.length > 0 ? (
            images.map((img, idx) => <img key={idx} src={img} className={`img-${idx}`} alt="news" />)
          ) : (
            <div className="placeholder-img">EchoNews AI</div>
          )}
        </div>
        
        <div className="card-controls">
          <button className={`icon-btn play ${isPlaying ? 'playing' : ''}`} onClick={handlePlayClick}>
            {isPlaying ? <Pause size={20} fill="white" /> : <Play size={20} fill="white" />}
          </button>
          <button className="icon-btn info" onClick={() => onOpenDetail(digest)}>
            <Info size={20} />
          </button>
        </div>

        {isPastNews && <span className="history-badge"><History size={12}/> 7-Day Vault</span>}
      </div>

      <div className="digest-content">
        <div className="digest-header">
           <span className="digest-tag">{label} BRIEF</span>
           <span className="date-text">{formattedDate}</span>
        </div>
        
        <ul className="headline-list">
          {headlines.slice(0, 3).map((h, i) => (
            <li key={`${h.title}-${i}`}>
              <ChevronRight size={12} className="bullet"/> {h.title}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};


export default DigestCard;