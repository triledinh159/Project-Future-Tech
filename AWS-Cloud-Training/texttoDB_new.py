import json
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb')

s3 = boto3.resource('s3')

s3_client=boto3.client('s3')

db_client=boto3.client('dynamodb')

def send_email_open():
    sns = boto3.client('sns')
    # The ARN of the SNS topic
    topic_arn = "arn:aws:sns:us-east-1:<topic>"

    # The message you want to send
    message = "Open Barrier OUT!!!"

    # Try to publish the message to the SNS topic
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message
        )
        print("Notification sent! Message ID:", response['MessageId'])
    except ClientError as e:
        print("Failed to send notification:", e)    
        
def send_email_alert():
    sns = boto3.client('sns')
    # The ARN of the SNS topic
    topic_arn = "arn:aws:sns:us-east-1:211125411054:check"

    # The message you want to send
    message = "ALERT!!! LICENSE PLATE IS MISMATCHED!!!"

    # Try to publish the message to the SNS topic
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message
        )
        print("Notification sent! Message ID:", response['MessageId'])
    except ClientError as e:
        print("Failed to send notification:", e)    

def lambda_handler(event, context):
    #take file
    bucket = event['Records'][0]['s3']['bucket']['name']
    fileName = event['Records'][0]['s3']['object']['key']
  
    client=boto3.client('rekognition')
  #processing image
  
    text=client.detect_text(Image={'S3Object': 
    {'Bucket':bucket,'Name':str(fileName)}})
    #updateLP
    res = s3_client.get_object(Bucket = bucket, Key=fileName)
  
    results = []

    for tF in text["TextDetections"]:
        if len(tF["DetectedText"]) > 0:
            results.append(tF["DetectedText"])
    if len(results)>4:
        finalResult =results[1] + '-' + results[2]
    else: finalResult = results[0] + '-' + results[1]
  
    table = dynamodb.Table('<DynamoDB-Table-name>')
  
    del_=fileName.find("_")
    
    ID=fileName[:-(len(fileName)-del_)] 
  
    data = db_client.get_item(
        TableName='<DynamoDB-Table-name>',
            Key={
            'ID': {
            'S': ID
            }
        }
  )
  
    #check existed
    if len(data) != 2: 
         return False
    else: 
        df=data["Item"]["LicensePlate"]["S"]
        if df == "":
            resp = table.update_item(
            Key={'ID': ID},
            UpdateExpression="SET LicensePlate= :s",
            ExpressionAttributeValues={':s': finalResult},
            ReturnValues="UPDATED_NEW")
            s3_client.delete_object(Bucket=bucket, Key=fileName)

            return "New"
        elif df == finalResult:
            s3_client.delete_object(Bucket=bucket, Key=fileName)
            resp = table.delete_item(
            Key={
            'ID': ID
          })

            return "Old"
        else :
            return True
