// Import required AWS SDK clients and commands for Node.js
import { QueryCommand } from "@aws-sdk/client-dynamodb";
import { ddbClient } from "../libs/ddbClient.mjs";
import { writeFile, existsSync} from "fs"
import { GetObjectCommand } from "@aws-sdk/client-s3";
import { S3Client } from "@aws-sdk/client-s3";// Helper function that creates Amazon S3 service client module.
const REGION = "us-east-1"; //e.g. "us-east-1"
// Create an Amazon S3 service client object.
const s3Client = new S3Client({ region: REGION });

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function download_image(path) {
  const bucketParams = {
    Bucket: "senior-design-images",
    Key: path,
  };
  try {
    // Create a helper function to convert a ReadableStream to a string.
    const streamToString = (stream) =>
      new Promise((resolve, reject) => {
        const chunks = [];
        stream.on("data", (chunk) => chunks.push(chunk));
        stream.on("error", reject);
        stream.on("end", () => resolve(Buffer.concat(chunks)));
      });

    // Get the object} from the Amazon S3 bucket. It is returned as a ReadableStream.
    const data = await s3Client.send(new GetObjectCommand(bucketParams));
    // Convert the ReadableStream to a string.
    const bodyContents = await streamToString(data.Body);
    writeFile("dist/assets/"+path, bodyContents,err3 => 
    {
        if (err3) {
        console.error(err3)
        return
        }
    })
    return 1
  } catch (err) {
    console.log("Error", err);
    return 0
  }
}


// Set the parameters
export const params = {
  KeyConditionExpression: "alertid = :a",
  // FilterExpression: "contains (Subtitle, :topic)",
  ExpressionAttributeValues: {
    ":a": { N: "123456" },
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
        'id':element.matchid.N,
        'x_coord':element.lat.S,
        'y_coord':element.lon.S,
        'image_name':element.img_path.S,
        'time':element.ts.S,
      }
      json_data['matches'].push(match)
      const content = JSON.stringify(json_data);
      try {
        if (!existsSync("dist/assets/"+element.img_path.S)){
          console.log("downloading asset from " + element.img_path.S)
          const k = download_image(element.img_path.S)
        }
      } catch (err) {
        console.log("Error", err);
        //const k = download_image(element.img_path.S)
      }
      
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
  await sleep(10000);
}
           

