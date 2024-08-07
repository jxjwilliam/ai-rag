import React, { useState } from 'react';
import axios from 'axios';

const ChatInterface = () => {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');

  const handleQueryChange = (e) => setQuery(e.target.value);

  const handleSendQuery = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/chat', query);
      setAnswer(response.data.answer);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSendQuery}>
        <input
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder="Ask a question..."
        />
        <button type="submit">Submit</button>
      </form>
      <div>{answer}</div>
    </div>
  );
};

export default ChatInterface;
