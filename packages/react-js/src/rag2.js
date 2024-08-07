import React, { useState } from 'react';
import axios from 'axios';

const QueryComponent = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/query', { query });
      setResult(response.data.answer);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
        />
        <button type="submit">Submit</button>
      </form>
      <p>{result}</p>
    </div>
  );
};

export default QueryComponent;
