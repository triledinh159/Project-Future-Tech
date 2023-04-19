import json
import boto3
import ast
from botocore.exceptions import ClientError
s3 = boto3.resource('s3')
def send_email():
    SENDER = "SENDER@mail.com" # must be verified in AWS SES Email
    RECIPIENT = "RECIPIENT@mail.com" # must be verified in AWS SES Email

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-southeast-1"

    # The subject line for the email.
    SUBJECT = "Open Barrier IN!!!"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Open Barrier IN!!!")
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Open Barrier IN!!!</h1>
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


        

s3_client = boto3.client('s3')

dynamodb_re = boto3.resource('dynamodb')

dy_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    #1. read data in bucket, init dyDB
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    
    json_file_name = event['Records'][0]['s3']['object']['key']
    
    json_object = s3_client.get_object(Bucket=bucket,Key=json_file_name)
    
    file_reader = json_object['Body'].read().decode("utf-8")
    
    file_reader = ast.literal_eval(file_reader)
    
    
    dynamodb_table = dynamodb_re.Table('basicData')
    
    #2. find the ID
    
    del_=json_file_name.find("_")
    
    ID=json_file_name[:-(len(json_file_name)-del_)] 
    
    data = dy_client.get_item(
        TableName='basicData',
        Key={
            'ID': {
            'S': ID
            }
        }
        
  )
  

     
    #3. check existed data
    
    if len(data) != 2:
        
        dynamodb_table.put_item(Item=file_reader)
        send_email()
        
        data1 = dy_client.get_item(
        TableName='basicData',
        Key={
            'ID': {
            'S': ID
            }
        }
        
  )

        src_bucket_path_2 = 'autocapt'
 
        src_file_name_2 = data1["Item"]["ID"]["S"] + '_' + data1["Item"]["Username"]["S"] + '.jpg'

        tgt_bucket_path_2 = bucket

        tgt_file_name_2 = data1["Item"]["ID"]["S"] + '_' + data1["Item"]["Username"]["S"] + '.jpg'

        copy_source_2 = {
        'Bucket': src_bucket_path_2,
        'Key': src_file_name_2
         }

        s3.meta.client.copy(copy_source_2, tgt_bucket_path_2, tgt_file_name_2)

        

    #else:
       #if (data["Item"]["ID"]["S"] != file_reader["ID"]) and (data["Item"]["Age"]["S"] != file_reader["Age"])  and (data["Item"]["ID"]["S"] != file_reader["ID"])
    s3_client.delete_object(Bucket=bucket, Key=json_file_name)