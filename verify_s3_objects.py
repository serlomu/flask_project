import boto3

s3 = boto3.client('s3', region_name='eu-north-1')
BUCKET_NAME = 'serlomucubo'

response = s3.list_objects_v2(Bucket=BUCKET_NAME)

for obj in response.get('Contents', []):
    print(obj['Key'])
