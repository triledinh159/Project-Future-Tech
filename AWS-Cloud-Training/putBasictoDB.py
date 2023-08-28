import json
import boto3
import ast
from botocore.exceptions import ClientError
s3 = boto3.resource('s3')

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
    
    
    dynamodb_table = dynamodb_re.Table('<DynamoDB-Table-name>')
    
    #2. find the ID
    
    del_=json_file_name.find("_")
    
    ID=json_file_name[:-(len(json_file_name)-del_)] 
    
    data = dy_client.get_item(
        TableName='<DynamoDB-Table-name>',
        Key={
            'ID': {
            'S': ID
            }
        }
        
  )
  

     
    #3. check existed data
    
    if len(data) != 2:
        
        dynamodb_table.put_item(Item=file_reader)
        
        data1 = dy_client.get_item(
        TableName='basicData',
        Key={
            'ID': {
            'S': ID
            }
        }
        
  )

        src_bucket_path_2 = '<name-bucket-store-image>'
 
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
