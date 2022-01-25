async function sendRequest(endpoint, data) {
    const requestOptions = {
      method: 'POST',
      headers: { 
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials" : true,
        'Content-Type': "multipart/form-data" 
        },
      body: JSON.stringify(data)
    };
    const response = await fetch('http://127.0.0.1:5000'+endpoint, requestOptions)
    const data = await response.json()
    return data
  }