## CSE 546 CC Project 2 - PaaS implementation using AWS Lambda

#### Group Name - Turing3

#### Group Members 
- Muskan Mehta (1225444701)
- Sannidhya Pathania (1225329976)
- Vaishnavi Amirapu (1225461211)

#### Group Members Tasks

1. Muskan Mehta
- Worked on the fetching the academic details from DynamoDB after performing face-recognition
- Worked on the code to output the results into a CSV file and upload it S3 bucket
- Created DynamoDB table and modified the given JSON file to conform with AWS format

2. Sannidhya Pathania
- Worked on the face_handler main function for the Lambda function
- Worked on looping through the frames to detect a face with known encoding
- Created an ECR repository to store docker images

3. Vaishnavi Amirapu
- Worked on frames_generation and frames_deletion implementation for the code
- Created and configured the Lambda funciton to trigger on the input S3 bucket for .mp4 files
- Ensured latest version of docker image is deployed on AWS Lambda


#### AWS Config
- region - us-east-1
- InputS3 - cse546-input
- OutputS3 - cse546-output
- DynamoDB table - cse546-ddb
- AccountID - 025635606453
- Lambda function - cse546-lambda-pj2
- AccessKeyID -<>
- SecretAccessKey - <>


