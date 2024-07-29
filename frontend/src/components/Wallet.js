import React, { useState } from 'react';
import { PublicKey, Connection, clusterApiUrl} from '@solana/web3.js';

const Wallet = () => {
  const [walletAddress, setWalletAddress] = useState(null);
  const [balance, setBalance] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [lobby, setLobby] = useState([]);
  const [secretWords, setSecretWords] = useState({});
  const [synonyms, setSynonyms] = useState({});

  const connectWallet = async () => {
    if (window.solana) {
      try {
        const response = await window.solana.connect();
        setWalletAddress(response.publicKey.toString());
      } catch (err) {
        console.error(err);
      }
    } else {
      alert('Solana wallet not found! Get a Phantom Wallet 👻');
    }
  };

  const getBalance = async () => {
    if (walletAddress) {
      // const connection = new Connection('https://api.devnet.solana.com'); // Connect to devnet
      const connection = new Connection(clusterApiUrl('devnet')); // Connect to devnet
      const publicKey = new PublicKey(walletAddress);
      const balance = await connection.getBalance(publicKey);
      setBalance(balance / 1e9); // Convert lamports to SOL
    }
  };

  const joinLobby = () => {
    if (walletAddress && !lobby.includes(walletAddress)) {
    setLobby([...lobby, walletAddress]);
    }
  };

  const startGame = () => {
    setGameStarted(true);
    console.log("Game has started!");
    const words = ['apple', 'banana', 'cherry', 'date', 'elderberry'];
    const selectedWords = {};
    const players = [...lobby];
    console.log("Players:", players);
    const randomIndex = Math.floor(Math.random() * players.length);
    players.forEach((player, index) => {
      if (index !== randomIndex) {
        selectedWords[player] = words[Math.floor(Math.random() * words.length)];
      }
    });
    setSecretWords(selectedWords);
  };

  return (
    <div>
      <button onClick={connectWallet}>Connect Wallet</button>
      {walletAddress && (
        <div>
          <p>Wallet Address: {walletAddress}</p>
          <button onClick={getBalance}>Get Balance</button>
          {balance !== null && <p>Balance: {balance} SOL</p>}
          <button onClick={joinLobby}>Join Lobby</button>
          <p>Players in Lobby: {lobby.length}</p>
              <ul>
                {lobby.map((player, index) => (
                  <li key={index}>{player}</li>
                ))}
              </ul>
          {!gameStarted && <button onClick={startGame}>Start Game</button>}
          {gameStarted && (
            <div>
              <p>Game Started!</p>
              {lobby.map((player, index) => (
                <div key={index}>
                  {secretWords[player] ? (
                    <div>
                      <p>Player {player}, your secret word is: {secretWords[player]}</p>
                      <input
                        type="text"
                        placeholder="Enter a synonym"
                        value={synonyms[player] || ''}
                      />
                    </div>
                  ) : (
                    <p>Player {player}, you don't have a secret word.</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Wallet;
