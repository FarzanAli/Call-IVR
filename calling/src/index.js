import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { makeCall, endCall, sendDigits } from './call.js';

const root = ReactDOM.createRoot(document.getElementById('root'));

const App = () => {
  return (
    <>
      <button onClick={() => makeCall()}>Start call</button>
      <button onClick={() => endCall()}>End Call</button>
      <button onClick={() => sendDigits(1)}>1</button>
      <button onClick={() => sendDigits(2)}>2</button>
      <button onClick={() => sendDigits(3)}>3</button>
      <button onClick={() => sendDigits(4)}>4</button>
      <button onClick={() => sendDigits(5)}>5</button>
      <button onClick={() => sendDigits(6)}>6</button>
      <button onClick={() => sendDigits(7)}>7</button>
      <button onClick={() => sendDigits(8)}>8</button>
      <button onClick={() => sendDigits(9)}>9</button>
    </>
  )
}
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
