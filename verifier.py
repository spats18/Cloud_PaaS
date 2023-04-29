import boto3

# AWS KEYS
AWS_ACCESS_KEY_ID = <secret key>
AWS_SECRET_ACCESS_KEY = <access key>

# Create an S3 client
s3_client = boto3.client('s3', 
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
                         region_name='us-east-1')
# Name of the S3 bucket
bucket_name = 'cse546-output'

# Count the number of CSV files in the S3 bucket
csv_count = 0
response = s3_client.list_objects_v2(Bucket=bucket_name)
print(response)
for obj in response['Contents']:
    if obj['Key'].lower().endswith('.csv'):
        csv_count += 1

print(f"Number of CSV files in {bucket_name}: {csv_count}")

# Print the contents of each CSV file in the S3 bucket
response = s3_client.list_objects_v2(Bucket=bucket_name)
for obj in response['Contents']:
    if obj['Key'].lower().endswith('.csv'):
        print(f"Contents of {obj['Key']}:")
        print(f"  Name   |   Major   |   Year")
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])
        csv_body = csv_obj['Body'].read().decode('utf-8')
        # print(csv_body)
        print(csv_body.split(" "))
        print("\n")
