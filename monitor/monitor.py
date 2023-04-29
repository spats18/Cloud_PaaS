import boto3
import json 
import urllib 



# Initialize the S3 client
s3_client = boto3.client('s3', 
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
                         region_name='us-east-1')
sqs_client  = boto3.client('sqs', 
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
                         region_name='us-east-1')
lambda_client  = boto3.client('lambda', 
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
                         region_name='us-east-1')

# Specify the S3 bucket name and Lambda function name
bucket_name = 'cse546-input'
lambda_function_name = 'cse546-lambda-pj2'
queue_url = "https://sqs.us-east-1.amazonaws.com/025635606453/s3-bucket-monitor-queue"
def delete_message(message: dict):
    '''
    Delete the input message from SQS queue
    '''
    delete_response = sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
    print(delete_response)
def long_poll_sqs():
    '''
    Long polling the SQS and get one message at a time
    '''
    response_obj = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, VisibilityTimeout=20,WaitTimeSeconds=10)
    # print('Response Object', response_obj)
    if "Messages" not in response_obj:
        print('No messages')
        return
    message_response = response_obj['Messages'][0]
#     print('message received')
    message_body = message_response['Body']
    print('Message Body',message_body)
    delete_message(message_response)
    return json.loads(message_body)





def monitor_call():
    print('Server started')
   
    while True:
        message = long_poll_sqs()
        # print('Mesasge polled from SQS\n', message)
        try:
            if message:
                # Catching 1 message at a time
                print(message)
                try:
                    record = message['Records'][0]
                    event_name = record['eventName']
                except Exception as e:
                    # print(f'Ignoring {message=} because of {str(e)}')
                    print('Ignoring S3 event message')
                    continue
                if event_name.startswith('ObjectCreated'):
                    # new file created!
                    s3_info = record['s3']
                    object_info = s3_info['object']
                    key = urllib.parse.unquote_plus(object_info['key'])
                    print(f'Found new object {key}')

                    # Invoke Lambda with this object and then delete the message 
                    response = lambda_client.invoke(
                        FunctionName=lambda_function_name,
                        Payload=json.dumps(message)
                    )

                    # Print the response from the Lambda function
                    print(response['Payload'].read())
        except Exception as e:
            print(f'error: {e}')

    
monitor_call()