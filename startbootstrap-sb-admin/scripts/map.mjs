// Import required AWS SDK clients and commands for Node.js
import { QueryCommand } from "@aws-sdk/client-dynamodb";
import { ddbClient } from "../libs/ddbClient.mjs";
import { writeFile} from "fs"
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Set the parameters
export const params = {
  KeyConditionExpression: "alertid = :a",
  // FilterExpression: "contains (Subtitle, :topic)",
  ExpressionAttributeValues: {
    ":a": { N: "1" },
  },
  ProjectionExpression: "alertid, matchid, lon, lat, ts, img_path",
  TableName: "Matches",
};

export const run = async () => {
  console.log('Updating')
  var json_data = {
    'matches':[]
  }
  try {

    const data = await ddbClient.send(new QueryCommand(params));
    data.Items.forEach(function (element, index, array) {
      console.log(element)
      var match = {
        'id':element.alertid.N,
        'x_coord':element.lat.N,
        'y_coord':element.lon.N,
        'image_name':element.img_path.S,
        'time':element.ts.N,
      }
      json_data['matches'].push(match)
      const content = JSON.stringify(json_data);

      writeFile('dist/test.json', content, err3 => 
      {
          if (err3) {
          console.error(err3)
          return
          }
      })
      console.log("Alert ID: " + element.alertid.N + ", Match ID: " + element.matchid.N + ", Longitude: " + element.lon.N + ", Latitude: " + element.lat.N);
    });
  return data
  } catch (err) {
    console.log("Error", err);
  }
};
while (1) {
  run();
  await sleep(2000);
}
           

