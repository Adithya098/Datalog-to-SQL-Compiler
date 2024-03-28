import React, { useState } from 'react';
import './styles.css';

function App() {
  const [textInput, setTextInput] = useState('');
  const [response, setResponse] = useState('');

  const handleInputChange = (event) => {
    setTextInput(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:5002/echo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
      });
      const data = await response.json();
      setResponse(data.echo);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleTranslate = async () => {
    try {
      const response = await fetch('http://localhost:5002/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
      });
      const data = await response.json();
      setResponse(data.translate);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="container">
      <h1>Compiler for Datalog to SQL</h1>
      <input
        type="text"
        value={textInput}
        onChange={handleInputChange}
        placeholder="Enter text here..."
      />
      <button onClick={handleTranslate}>Submit</button>
      {/* <button onClick={handleSubmit}>Submit</button> */}
      <p>Response: {response}</p>
    </div>
  );
}

export default App;
