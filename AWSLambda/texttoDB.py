import json
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb')

s3 = boto3.resource('s3')

s3_client=boto3.client('s3')

db_client=boto3.client('dynamodb')

def send_email_open():
    SENDER = "SENDER@mail.com" # must be verified in AWS SES Email
    RECIPIENT = "RECIPIENT@mail.com" # must be verified in AWS SES Email

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-southeast-1"

    # The subject line for the email.
    SUBJECT = "Open Barrier OUT !!!"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Open Barrier OUT !!!")
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Open Barrier OUT!!!</h1>
    <p></p>
    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
        
                        'Data': BODY_HTML
                    },
                    'Text': {
        
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {

                    'Data': SUBJECT
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        
def send_email_alert():
    SENDER = "SENDER@mail.com" # must be verified in AWS SES Email
    RECIPIENT = "RECIPIENT@mail.com" # must be verified in AWS SES Email

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-southeast-1"

    # The subject line for the email.
    SUBJECT = "ALERT !!!"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("ALERT !!!")
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1> LICENSE PLATE IS MISMATCHED!!!</h1>
    <p></p>
    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
        
                        'Data': BODY_HTML
                    },
                    'Text': {
        
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {

                    'Data': SUBJECT
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])        

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
  
    table = dynamodb.Table('basicData')
  
    del_=fileName.find("_")
    
    ID=fileName[:-(len(fileName)-del_)] 
  
    data = db_client.get_item(
        TableName='basicData',
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
            send_email_open()

            return "Old"
        else :
            send_email_alert()
            return True
