import boto3
import face_recognition
import pickle
import os
import ffmpeg
import boto3
import csv
import shutil

input_bucket = "cse546-input"
output_bucket = "cse546-output"
dynamodb_table = "cse546-ddb"
frames_path = '/tmp/'

AWS_ACCESS_KEY_ID = 'AKIAQL6AAJ62SU3E4WMV'
AWS_SECRET_ACCESS_KEY = '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'

s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
dynamodb_client = boto3.client('dynamodb',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key= AWS_SECRET_ACCESS_KEY,region_name='us-east-1')
				
# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def download_video_s3(video_name):
	print("Downloading video")
	s3_client.download_file(Bucket=input_bucket, Key=video_name, Filename='/tmp/'+video_name)
	print("Extracting frames from video")
	os.system("ffmpeg -i " + str('/tmp/'+video_name) + " -r 1 " + str(frames_path) + "image-%3d.jpeg")
	print("Frames extracted")


def get_item(name,video_name):

	response = dynamodb_client.scan(TableName=dynamodb_table,IndexName='name-index')
	#print(response)
	value_list=[]
	for item in response['Items']:
		if item['name']['S']==name:
			print(item)
			for i in item.values():
				print(i)
				if 'S' in i:
					value_list.append(i['S'])
	output_csv=video_name.split(".")[0]+".csv"
	print("File name:", output_csv, video_name)
	
	with open('/tmp/'+output_csv, 'w', newline='') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		wr.writerow(value_list)
	
	response=s3_client.upload_file('/tmp/'+output_csv, output_bucket, output_csv)
	print("upload response: ", response)

def frames_deletion():
	# clear frames
	for filename in os.listdir(frames_path):
		file_path = os.path.join(frames_path, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))


def face_recognition_handler(event, context):	
	print("Hello")
	data = open_encoding('encoding')
	known_names = data['name']
	given_encoding = data['encoding']
	print("in between encoding and download s3")

	video_name=event['Records'][0]['s3']['object']['key']
	download_video_s3(video_name)
	face_recognition_result = ""

	for filename in os.listdir(frames_path):
		if filename.endswith(".jpeg"):
			unknown_image = face_recognition.load_image_file(frames_path+filename)
			new_encoding = face_recognition.face_encodings(unknown_image)[0]
			results = face_recognition.compare_faces(given_encoding, new_encoding)
			if True in results:
				first_match_index = results.index(True)
				face_recognition_result = known_names[first_match_index]
				break

	print("Result of face recognition:", face_recognition_result)
	get_item(face_recognition_result,video_name)
	frames_deletion()