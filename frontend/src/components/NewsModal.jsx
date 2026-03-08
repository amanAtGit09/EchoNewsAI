import React from 'react';
import { X, ExternalLink, User, Globe } from 'lucide-react';

const NewsModal = ({ digest, onClose }) => {
  // FIX: If digest is an array, grab the first item
  const data = Array.isArray(digest) ? digest[0] : digest;
  
  // Safety check: If data or Headlines is missing, don't render anything
  if (!data || !data.Headlines) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-modal" onClick={onClose}><X size={20}/></button>
        
        <div className="modal-header">
          <h2 style={{ color: '#00d4ff' }}>Detailed Coverage</h2>
          <p className="modal-subtitle">{data.Headlines.length} Stories summarized by Echo AI</p>
        </div>

        <div className="modal-body">
          {data.Headlines.map((h, idx) => (
            <div key={idx} className="modal-news-item">
              {/* IMAGE: Fixed with the 'image' key from your console log */}
              {h.image && <img src={h.image} className="modal-item-img" alt="" />}
              
              <div className="modal-item-info">
                <div className="source-row">
                  {/* SOURCE ICON: Using the rich metadata from your log */}
                  {h.source_icon && <img src={h.source_icon} className="source-icon" alt="" />}
                  <span style={{ fontWeight: 'bold' }}>{h.source_name || h.source_id}</span>
                  {h.author && <span className="author-tag"><User size={12}/> {h.author}</span>}
                </div>
                
                <h3 style={{ margin: '10px 0', fontSize: '18px' }}>{h.title}</h3>
                <p style={{ color: '#ccc', lineHeight: '1.5' }}>{h.description}</p>
                
                <a href={h.link} target="_blank" rel="noreferrer" className="read-more-link">
                  View Full Source <ExternalLink size={14} />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default NewsModal;