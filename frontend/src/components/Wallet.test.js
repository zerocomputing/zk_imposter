// Wallet.test.js
const { useState } = require('react');

// Mock the setLobby function
let lobby = [];
const setLobby = (newLobby) => {
  lobby = newLobby;
};

// Function to add a wallet address to the lobby
const addWalletToLobby = (walletAddress) => {
  if (walletAddress && !lobby.includes(walletAddress)) {
    setLobby([...lobby, walletAddress]);
  }
};

// Function to generate a random wallet address
const generateRandomAddress = () => {
  return 'address_' + Math.random().toString(36).substr(2, 9);
};

// Jest test case
test('multiple players joining the lobby', () => {
  // Reset lobby before each test
  lobby = [];

  // Simulate multiple players joining
  const walletAddresses = ['address1', 'address2', 'address3'];
  walletAddresses.forEach(addWalletToLobby);

  // Verify the lobby contains all the added addresses
  expect(lobby).toEqual(walletAddresses);
});

// Jest test case
test('multiple players joining the lobby with random addresses', () => {
  // Reset lobby before each test
  lobby = [];

  // Generate multiple random wallet addresses
  const walletAddresses = Array.from({ length: 5 }, generateRandomAddress);

  // Simulate multiple players joining
  walletAddresses.forEach(addWalletToLobby);

  // Verify the lobby contains all the added addresses
  expect(lobby).toEqual(walletAddresses);
});
