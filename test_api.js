const axios = require('axios');

// Simple test to verify the API endpoints are accessible
async function testApiEndpoints() {
  try {
    // Test the root endpoint
    const rootResponse = await axios.get('http://localhost:8000/');
    console.log('Root endpoint status:', rootResponse.status);

    // Test the health endpoint
    const healthResponse = await axios.get('http://localhost:8000/health');
    console.log('Health endpoint status:', healthResponse.status);

    // Test the chat endpoint (should return 422 since we're not sending proper data)
    try {
      const chatResponse = await axios.post('http://localhost:8000/api/v1/chat/', {});
    } catch (error) {
      if (error.response && error.response.status === 422) {
        console.log('Chat endpoint accessible (expected 422 for missing data)');
      } else {
        console.error('Unexpected error calling chat endpoint:', error.message);
      }
    }

    console.log('API endpoints are accessible');
  } catch (error) {
    console.error('Error testing API endpoints:', error.message);
  }
}

testApiEndpoints();