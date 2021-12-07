// Load the required clients and packages
const { CognitoIdentityClient } = require("@aws-sdk/client-cognito-identity");
const {
  fromCognitoIdentityPool,
} = require("@aws-sdk/credential-provider-cognito-identity");
const { S3Client, ListObjectsCommand } = require("@aws-sdk/client-s3");

// Initialize the Amazon Cognito credentials provider
const REGION = "us-east-1";
const s3 = new S3Client({
  region: REGION,
  credentials: fromCognitoIdentityPool({
    client: new CognitoIdentityClient({ region: REGION }),
    identityPoolId: "us-east-1:990518e8-05cf-44b7-b8f2-c25c4f67ed0c", // IDENTITY_POOL_ID e.g., eu-west-1:xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx
  }),
});

// Use getHTML to find image HTML attribute and populate
// See: https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/s3-example-photos-view.html