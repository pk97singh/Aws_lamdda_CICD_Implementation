
# 📡 AWS S3 File Processing Notifications

This project implements an **event-driven system** using **Amazon S3, AWS Lambda, and Amazon SNS** to monitor file arrivals and processing status in an S3 bucket.

Whenever a file is uploaded to the S3 bucket, a Lambda function is triggered to:

1. Capture **file details** (name, bucket, timestamp).
2. Check **processing status** (Success / Failure).
3. Send an **email notification** via SNS with the results.

---

## 🔧 Architecture

```
[S3 Bucket] ---> [Lambda Function] ---> [SNS Topic] ---> [Email Notification]
```

---

## 📂 Features

* Event-driven (no polling required).
* Sends **structured email** with:

  * File name
  * Bucket name
  * Processing status
  * Timestamp
* Supports both **SUCCESS** ✅ and **FAILURE** ❌ messages.
* Easily extendable to log results in DynamoDB, CloudWatch, or QuickSight dashboards.

---

## 🚀 Setup Instructions

### 1. Create an S3 Bucket

```bash
aws s3 mb s3://snsdemoprabhat
```

### 2. Create an SNS Topic

```bash
aws sns create-topic --name FileProcessingTopic
```

Subscribe your email:

```bash
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:<account-id>:FileProcessingTopic \
  --protocol email \
  --notification-endpoint youremail@example.com
```

Confirm the email subscription.

---

### 3. Deploy Lambda Function

Example Lambda code (`lambda_function.py`):

```python
import boto3
import datetime

sns = boto3.client('sns')
TOPIC_ARN = "arn:aws:sns:us-east-1:<account-id>:FileProcessingTopic"

def lambda_handler(event, context):
    # Extract file info from S3 event
    file_obj = event['Records'][0]['s3']
    bucket = file_obj['bucket']['name']
    file_name = file_obj['object']['key']

    # Simulated status (can be dynamic)
    status = "SUCCESS"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build message
    message = f"""
    File Processing Status: {status}
    File: {file_name}
    Bucket: {bucket}
    Time: {timestamp}
    """

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject=f"{status} - Daily Data Processing",
        Message=message
    )

    return {"statusCode": 200, "body": "Notification sent"}
```

Zip & upload:

```bash
zip function.zip lambda_function.py
aws lambda create-function \
  --function-name FileProcessingLambda \
  --runtime python3.9 \
  --role arn:aws:iam::<account-id>:role/<lambda-role> \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

---

### 4. Add S3 Trigger

* Go to S3 bucket → **Properties** → **Event notifications**.
* Configure event for `PUT` (file upload).
* Link it to the Lambda function.

---

## 📧 Sample Email Notification

```
File Processing Status: SUCCESS
File: Global+Health+Statistics.csv
Bucket: snsdemoprabhat
Time: 2025-08-24 11:53:15
```

---

## 📊 Future Enhancements

* Separate **Success / Failure** SNS topics.
* Store processing logs in **DynamoDB**.
* Add monitoring dashboards in **CloudWatch** or **QuickSight**.
* Support Slack/Teams notifications via SNS HTTP subscriptions.

---

✅ With this setup, you get **real-time monitoring** of your S3 file pipelines with **zero manual effort**.

---

👉 Do you want me to also include **README screenshots (email alerts + architecture diagram)** so it looks more professional on GitHub?
