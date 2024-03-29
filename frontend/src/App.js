import React, { useState } from 'react';
import './styles.css';

function App() {
  const [textInput, setTextInput] = useState('');
  const [response, setResponse] = useState('');
  const [dbResponse, setdbResponse] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [database, setDatabase] = useState('');
  const [port, setDatabasePort] = useState(5432);


  const handleInputChange = (event) => {
    setTextInput(event.target.value);
  };

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleDatabaseChange = (event) => {
    setDatabase(event.target.value);
  };

  const handleDatabasePortChange = (event) => {
    setDatabasePort(event.target.value);
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
        body: JSON.stringify({ text: textInput}),
      });
      const data = await response.json();
      console.log(data.translate)
      setResponse(data.translate);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleExecute = async () => {
    try {
      const response = await fetch('http://localhost:5002/execute_query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput , password: password, username: username, database: database, port: port}),
      });
      const data = await response.json();
      console.log(data.execute_query)
      setdbResponse(data.execute_query);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="container">
      <h1>Compiler for Datalog to SQL</h1>
      <input
        type="text"
        value={database}
        onChange={handleDatabaseChange}
        placeholder="Database Name"
      />
      <input
        type="text"
        value={username}
        onChange={handleUsernameChange}
        placeholder="Postgres Username"
      />
      <input
        type="password"
        value={password}
        onChange={handlePasswordChange}
        placeholder="Postgres Password"
      />
      <input
        type="text"
        value={port}
        onChange={handleDatabasePortChange}
        placeholder="Port Number"
      />
      <input
        type="text"
        value={textInput}
        onChange={handleInputChange}
        placeholder="Enter your datalog query here.."
      />
      <button onClick={handleTranslate}>Translate</button>
      <div className="response-container">
        <h2>Response:</h2>
        {response && response.map((responseItem, index) => (
          <p key={index} className="response-item">{responseItem}</p>
        ))}
      </div>
      <button onClick={handleExecute}>Execute SQL Query</button>
      <div className="response-container">
        <h2>DB Response:</h2>
        <p>{dbResponse}</p>
      </div>
    </div>
  );  
}

export default App;
