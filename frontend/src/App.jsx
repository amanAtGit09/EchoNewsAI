import React, { useState } from 'react';
import { Search, Radio, RefreshCw, History, X } from 'lucide-react';
import CategoryRow from './components/CategoryRow';
import NewsModal from './components/NewsModal'; // Import the new Modal
import { fetchNews } from './api';

function App() {
  const [searchResults, setSearchResults] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [currentAudio, setCurrentAudio] = useState(null);
  const [recentSearches, setRecentSearches] = useState(() => {
  return JSON.parse(localStorage.getItem('recentSearches')) || [];
  });
  // State for the floating detail tab (Modal)
  const [selectedDigest, setSelectedDigest] = useState(null);

  const handleSearch = async (e, term = null) => {
    // Only call preventDefault if the event object exists
    if (e) e.preventDefault();
    
    // Use the passed term (from tags) or the current search query
    const query = term || searchQuery;
    if (!query.trim()) return;

    // Save to history
    const updatedHistory = [query, ...recentSearches.filter(s => s !== query)].slice(0, 5);
    setRecentSearches(updatedHistory);
    localStorage.setItem('recentSearches', JSON.stringify(updatedHistory));

    setIsSearching(true);
    const data = await fetchNews({ type: 'pipeline', q: query });
    if (data) {
      // [data, ...prev] puts the newest search card at the very beginning of the row
      setSearchResults(prev => [data, ...(prev || [])]);
    }
    setIsSearching(false);
  };

  // // ... inside return ...
  // {selectedDigest && (
  //   <NewsModal 
  //     // Ensure we pass the FIRST item if selectedDigest happens to be an array
  //     digest={Array.isArray(selectedDigest) ? selectedDigest[0] : selectedDigest} 
  //     onClose={() => setSelectedDigest(null)} 
  //   />
  // )}

  return (
    <div className="app-container">
      {/* 1. Header & Search */}
      <header className="main-header">
        <div className="logo">
          <Radio color="#00d4ff" size={28} />
          <span>EchoNewsAI</span>
        </div>
        
        <form onSubmit={handleSearch} className={`search-box ${isSearching ? 'searching' : ''}`}>
        <input 
          type="text" 
          placeholder={isSearching ? "Echo is searching..." : "Search news by keyword..."} 
          value={searchQuery}
          disabled={isSearching}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="submit">
          {isSearching ? <RefreshCw className="spin" size={18} /> : <Search size={18} />}
        </button>
        </form>

        <div className="recent-searches">
          {recentSearches.map((term, i) => (
            <button 
              key={i} 
              className="search-tag"
              onClick={() => {
                setSearchQuery(term);
                handleSearch(null, term); // Pass term directly
              }}
            >
              <History size={12} /> {term}
            </button>
          ))}
        </div>
      </header>

      <main>
        {/* Search Results */}
        {searchResults && (
        <section className="search-results-container">
          <div className="search-header">
            <h2>Your Search Results</h2>
            <button onClick={() => setSearchResults(null)} className="clear-btn">Clear</button>
          </div>
          <CategoryRow 
            initialData={searchResults} 
            isSearch={true}
            onPlay={setCurrentAudio}
            currentAudio={currentAudio}
            onOpenDetail={setSelectedDigest}
          />
        </section>
      )}

        {/* Categorized Netflix Rows */}
        <section className="briefing-section">
        <CategoryRow 
          title="Daily Briefing" 
          category="breaking" 
          isSearch={true}
          isBriefing={true} 
          onPlay={setCurrentAudio} 
          currentAudio={currentAudio} 
          onOpenDetail={setSelectedDigest} 
        />
        </section>

        {/* The Briefing Section */}
        <CategoryRow 
          title="Trending Now" 
          category="top" 
          onPlay={setCurrentAudio}
          currentAudio={currentAudio}
          onOpenDetail={setSelectedDigest} // Open Modal logic
        />

        {/* Categorized Netflix Rows */}
        <CategoryRow 
          title="Technology" 
          category="technology" 
          onPlay={setCurrentAudio} 
          currentAudio={currentAudio} 
          onOpenDetail={setSelectedDigest} 
        />
        <CategoryRow 
          title="Sports" 
          category="sports" 
          onPlay={setCurrentAudio} 
          currentAudio={currentAudio} 
          onOpenDetail={setSelectedDigest} 
        />
        <CategoryRow 
          title="Business" 
          category="business" 
          onPlay={setCurrentAudio} 
          currentAudio={currentAudio} 
          onOpenDetail={setSelectedDigest} 
        />
        <CategoryRow 
          title="Politics" 
          category="politics" 
          onPlay={setCurrentAudio} 
          currentAudio={currentAudio} 
          onOpenDetail={setSelectedDigest} 
        />
      </main>

      {/* Hidden Audio Player */}
      {currentAudio && (
        <audio 
          src={currentAudio} 
          autoPlay 
          onEnded={() => setCurrentAudio(null)} 
        />
      )}

      {/* Floating Detail Tab (Modal) */}
      {selectedDigest && (
        <NewsModal 
          digest={selectedDigest} 
          onClose={() => setSelectedDigest(null)} 
        />
      )}
    </div>
  );
}

export default App;