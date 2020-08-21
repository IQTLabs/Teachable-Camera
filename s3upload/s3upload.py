import os
import boto3
import time
import shutil
from botocore.exceptions import ClientError
import json

image_path = "/capture"
archive_path = "/archive"
bucket_name = ''
expiration = 3600

print(os.getenv('ACCESS_KEY'))
s3_client = boto3.client('s3', aws_access_key_id=os.getenv('ACCESS_KEY'), aws_secret_access_key=os.getenv('SECRET_KEY'))


def manualLogin(_aws_access_key_id,_aws_secret_access_key):
    global s3_client
    s3_client = boto3.client('s3', aws_access_key_id=_aws_access_key_id, aws_secret_access_key=_aws_secret_access_key)


def archiveFile(file_path,archive_path):
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    shutil.move(file_path, os.path.join(archive_path, os.path.basename(file_path)))

    
def presignedURL(object_name):
    response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name,'Key': object_name}, ExpiresIn=expiration)
    return response


def uploadFile(file_path, bucket):
    object_name = os.path.basename(file_path)

    try:
        response = s3_client.upload_file(file_path, bucket, object_name)
        response = presignedURL(object_name)
        response = createJSON(object_name, ['bear'], presignedURL(object_name))
    except ClientError as e:
        return False
    return response


def createJSON(file_path, labels, url):
    tmp = {}
    tmp['filename'] = file_path
    tmp['labels'] = labels
    tmp['url'] = url
    return tmp

def uploadDirectory(image_path, archive_path):
    for file in os.listdir(image_path):
        file_full_path = os.path.join(image_path, file)
        archive_path_tmp = os.path.join(archive_path, file[15:25])

        uploadFile(file_full_path, bucket_name)
        archiveFile(file_full_path,archive_path_tmp)

        
def uploadImage(file_full_path, json_file_full_path):
    with open(json_file_full_path) as f:
        data = json.load(f)
    labelsOut = []
    for record in data:
        labelsOut.append(record['label'])
    archive_path_tmp = os.path.join(archive_path, file_full_path.split('_')[1][0:10])
    
    response = uploadFile(json_file_full_path, bucket_name)
    response = uploadFile(file_full_path, bucket_name)
    response['labels'] = labelsOut
    response = json.dumps(response)
    print(response)
    archiveFile(json_file_full_path, archive_path_tmp)
    archiveFile(file_full_path, archive_path_tmp)
    
    return response

