// Import required AWS SDK clients and commands for Node.js
import { BatchGetItemCommand } from "@aws-sdk/client-dynamodb";
import { ddbClient } from "../libs/ddbClient.js";

// Set the parameters
export const params = {
  RequestItems: {
    Matches: {
      Keys: [
        {
            alertid: { N: "1" },
            matchid: { N: "1" },
        },
      ],
      ProjectionExpression: "img_path, lat, lon",
    },
  },
};

export const run = async () => {
  try {
    const data = await ddbClient.send(new BatchGetItemCommand(params));
    console.log("Success, items retrieved", data.Responses.Matches);
    return data;
  } catch (err) {
    console.log("Error", err);
  }
};
run();
           

