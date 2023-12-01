const WebSocket = require('ws');

const socket = new WebSocket('ws://localhost:5008');

socket.onopen = (event) => {
  console.log('Connected to the WebSocket server:', event);
};

socket.onmessage = (event) => {
  const message = event.data;
  console.log('Received a message:', message);
};

socket.onclose = (event) => {
  if (event.wasClean) {
    console.log(`Connection closed cleanly, code=${event.code}, reason=${event.reason}`);
  } else {
    console.error('Connection died');
  }
};

socket.onerror = (error) => {
  console.error('WebSocket Error:', error);
};
