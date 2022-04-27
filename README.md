# Electri

Electri is a service for automating, maximizing, and streamlining data sourcing for vehicle-centered AMBER alerts.

## To run the front end website and service
- Navigate to the `/startboostrap-sb-admin` folder
- Start up the npm server by running : npm run start
- When step 2 is complete, start up the flask server by running `export FLASK_APP=scripts/app.py` then `flask run`
- Now the website is running on localhost port 3000 on your device. You can view the public website or log in as a verified user to view the dashboard pages. 
    - There exists some dummy data in our database. You can login as a verified user with username “admin” and password “admin”.
- Install the aws cli client on whatever OS you are using
- Get aws secret keys for user electri from the aws console, see <a href="https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys">here</a>
- In the command line run: `aws configure` and input the credentials from step 5b
- To upload an image navigate to `/image_detection` and run `pip install boto3` then `python client_upload.py e 
- The image will be processed and if there is an active alert it matches, it will show up on the map page

