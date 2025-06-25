import boto3
import json
import os
from datetime import datetime

s3 = boto3.client('s3')
ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['DDB_TABLE'])
BUCKET = os.environ['S3_BUCKET']

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    method = event['httpMethod']
    path = event.get('resource', event.get('path', ''))
    body = json.loads(event['body']) if event.get('body') else {}

    if method == 'OPTIONS':
        return build_response(200)

    if path in ['/list', '/status'] and method == 'GET':
        return list_files()
    elif path == '/lock' and method == 'POST':
        return lock_file(body)
    elif path == '/unlock' and method == 'POST':
        return unlock_file(body)
    elif path == '/get-url' and method == 'POST':
        return generate_presigned_url(body)
    elif path == '/s3-files' and method == 'GET':
        return list_s3_files()
    else:
        return build_response(400, "Unsupported operation")

def build_response(status, body=None):
    return {
        'statusCode': status,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body) if body is not None else ''
    }

def list_files():
    try:
        resp = table.scan()
        return build_response(200, resp['Items'])
    except Exception as e:
        return build_response(500, {'error': str(e)})

def lock_file(body):
    try:
        filename = body['filename']
        user = body['user']
        now = datetime.utcnow().isoformat()

        resp = table.get_item(Key={'filename': filename})
        if 'Item' in resp and resp['Item']['status'] == 'locked':
            return build_response(409, 'File is already locked')

        table.put_item(Item={
            'filename': filename,
            'status': 'locked',
            'locked_by': user,
            'timestamp': now
        })
        return build_response(200, 'File locked')
    except Exception as e:
        return build_response(500, {'error': str(e)})

def unlock_file(body):
    try:
        filename = body['filename']
        table.update_item(
            Key={'filename': filename},
            UpdateExpression='SET #s = :s REMOVE locked_by',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':s': 'unlocked'}
        )
        return build_response(200, 'File unlocked')
    except Exception as e:
        return build_response(500, {'error': str(e)})

def generate_presigned_url(body):
    try:
        filename = body['filename']
        action = body['action']
        if action == 'get':
            url = s3.generate_presigned_url('get_object',
                Params={'Bucket': BUCKET, 'Key': filename}, ExpiresIn=3600)
        else:
            url = s3.generate_presigned_url('put_object',
                Params={'Bucket': BUCKET, 'Key': filename}, ExpiresIn=3600)
        return build_response(200, {'url': url})
    except Exception as e:
        return build_response(500, {'error': str(e)})

def list_s3_files():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return build_response(200, files)
    except Exception as e:
        return build_response(500, {'error': str(e)})
