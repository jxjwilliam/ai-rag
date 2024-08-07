// Example React.js code
import axios from 'axios';

const handleSubmit = async (query) => {
  try {
    const response = await axios.post('http://localhost:8000/chat', { query });
    console.log(response.data.response);
  } catch (error) {
    console.error('Error:', error);
  }
};
