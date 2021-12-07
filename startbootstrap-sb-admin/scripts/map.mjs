// Import required AWS SDK clients and commands for Node.js
import { QueryCommand } from "@aws-sdk/client-dynamodb";
import { ddbClient } from "../libs/ddbClient.mjs";

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
  ProjectionExpression: "alertid, matchid, lon, lat",
  TableName: "Matches",
};

export const run = async () => {
  try {
  const data = await ddbClient.send(new QueryCommand(params));
  data.Items.forEach(function (element, index, array) {
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
           

