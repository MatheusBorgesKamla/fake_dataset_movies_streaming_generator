from dotenv import load_dotenv
import logging
from os import getenv
import boto3
import datetime
from botocore.exceptions import ClientError

def get_bucket(path_bucket, client):
    try:
        client.create_bucket(Bucket=path_bucket)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    

def ingest_file(path_file, path_bucket, client, specified_key = None):
    if specified_key is None:
        specified_key = path_file

    try:
        client.upload_file(path_file, path_bucket, specified_key)
    except ClientError as e:
        logging.error(e)
        return False
    return True

load_dotenv("/home/matheus/.env")

env_keys = {
    "aws_id" :  getenv("AWS_ID"),
    "aws_key" :  getenv("AWS_KEY"),
    "aws_account" : getenv("AWS_ACCOUNT")
}

s3_client = boto3.client(
    's3',
    aws_access_key_id = env_keys["aws_id"],
    aws_secret_access_key = env_keys["aws_key"],
)

bucket_name = env_keys["aws_account"] + "-landing-zone"


if get_bucket(bucket_name, s3_client):
    print("Creating/getting AWS "+bucket_name+" with success")

files = [{"local_path":"users_dataset.csv",
          "s3_path":"users/users_dataset.csv" 
         },
         {"local_path":"movies_events.json",
          "s3_path":"movies_events/movies_events_dataset.json"
         }]

"movies_events.json"
for f in files:
    if ingest_file(f["local_path"], bucket_name, s3_client, f["s3_path"]):
        print(f"Uploading {f['local_path']} in {bucket_name} bucket with success")
