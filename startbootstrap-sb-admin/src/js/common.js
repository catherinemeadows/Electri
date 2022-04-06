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

async function getMatchesByAlertId(){

}

async function getAllMatches(){

}

function getCircle(matches){
  var circleData = {'longitude':0, 'latitude':0,'radius':0}
  for (var i = 0; i < matches.length; i++) {
    circleData.longitude += matches[i].longitude
    circleData.latitude += matches[i].latitude
  } 
  circleData.longitude /= matches.length
  circleData.latitude /= matches.length

  // calculate radius 
  var max_distance = 0
  for (var i = 0; i < matches.length; i++) {
    var distance = Math.sqrt(Math.pow(circleData.longitude - matches[i].longitude,2) + Math.pow(circleData.latitude - matches[i].latitude,2))
    if (distance > max_distance) {
      max_distance = distance
    }
  }
  circleData.radius = max_distance * 111000
  return circleData
}
