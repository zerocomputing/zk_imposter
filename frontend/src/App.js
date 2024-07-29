import React from 'react';
import Wallet from './components/Wallet';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to ZK Imposter</h1>
        <Wallet />
      </header>
    </div>
  );
}

export default App;
