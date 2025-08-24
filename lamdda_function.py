import boto3
import json
import datetime

sns = boto3.client('sns')

def lambda_handler(event, context):
    file_name = event['Records'][0]['s3']['object']['key']
    bucket = event['Records'][0]['s3']['bucket']['name']
    status = "SUCCESS"  # or dynamically detect
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""
    File Processing Status: {status}
    File: {file_name}
    Bucket: {bucket}
    Time: {timestamp}
    """
    
    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:065054231720:demosns",
        Subject=f"{status} - Daily Data Processing",
        Message=message
    )
