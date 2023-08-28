import json
import boto3

dynamodb_client = boto3.resource('dynamodb')
s3 = boto3.resource('s3')
client = boto3.client('dynamodb')
def lambda_handler(event, context):

    #1. set query
    
    ins_id = event['queryStringParameters']['userID']
    ins_name = event['queryStringParameters']['username']
    ins_res = {}
    ins_res['userID'] = ins_id
    ins_res['username'] = ins_name
    
    #2. copy user basic data from source to target
    
    src_bucket_path = 'triuserdata'
    src_file_name = ins_res['userID'] + '_' + ins_res['username'] + '.json'
    tgt_bucket_path = 'tricheckdata'
    tgt_file_name = ins_res['userID'] + '_' + ins_res['username'] +'.json'
    copy_source = {
    'Bucket': src_bucket_path,
    'Key': src_file_name
    }
    #3. Copy user license plate from source to target

    src_bucket_path_2 = 'imagecap'
    src_file_name_2 = ins_res['userID'] + '_' + ins_res['username'] + '.jpg'
    tgt_file_name_2 = ins_res['userID'] + '_' + ins_res['username'] +'.jpg'
    copy_source_2 = {
    'Bucket': src_bucket_path_2,
    'Key': src_file_name_2
    }
 
    
    
    # TODO implement
    
    
    dynamodb_table = dynamodb_client.Table('basicData')
    
    data = client.get_item(
        TableName='basicData',
        Key={
            'ID': {
            'S': ins_res['userID']
            }
        }
  )
    # check in-out status
    if len(data) == 2: 
        s3.meta.client.copy(copy_source_2, tgt_bucket_path, tgt_file_name_2)
        return {
            'statusCode': 200,
            'body': json.dumps('Checking success! Please wait for signal!')
    } #this is check for existed data and let's user go outside
    else: 
        s3.meta.client.copy(copy_source, tgt_bucket_path, tgt_file_name)
        return {
            'statusCode': 200,
            'body': json.dumps('Transaction success!')
    } # go inside      
