async function sendRequest(endpoint, data) {
    data.token = localStorage.getItem('token')
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
    const ret_data = await response.json()
    return ret_data['data']
  }
async function logout(){
  console.log("logging out")
  if (localStorage.getItem('token') !== null) {        
      sendRequest('/logout', {}) 
      localStorage.removeItem('token');
      console.log(localStorage)
  }
  window.location.pathname = "/login.html"  
}

async function getCurrentMatches(alert_filters){
  data = await sendRequest('/getMatches', {'alerts':alert_filters}) 
  return data
}

async function getAlerts(){
  data = await sendRequest('/getAlerts',{}) 
  return data
}
async function addAlert(alertData){ 
  
  data = await sendRequest('/insertAlert', alertData)
}

async function registerUser(){

}

async function getMatchesByAlertId(){

}

async function getAllMatches(){

}
