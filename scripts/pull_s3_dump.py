import boto3
import getpass
import os
from botocore.config import Config
sts = boto3.client('sts', config=Config(proxies={
    'http': 'http://192.168.7.4:8080',
    'https': 'http://192.168.7.4:8080',
}), verify=False)
token = getpass.getpass("Enter MFA Token: ")
response = sts.get_session_token(
    DurationSeconds=129600,
    SerialNumber='arn:aws:iam::389904390004:mfa/nilabja.ray@dcbbank.com',
    TokenCode=token)
access_key_id = response['Credentials']['AccessKeyId']
secret_access_key = response['Credentials']['SecretAccessKey']
session_token = response['Credentials']['SessionToken']
region_name = "ap-southeast-1"
session = boto3.session.Session(access_key_id, secret_access_key, session_token,
                      region_name)
s3 = session.client('s3', config=Config(proxies={
    'http': 'http://192.168.7.4:8080',
    'https': 'http://192.168.7.4:8080',
}), verify=False)
# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
# buckets = [bucket['Name'] for bucket in response['Buckets']]

# Print out the bucket list
# print("Bucket List: {}".format("\n".join(buckets)))

list=s3.list_objects(Bucket='dcb-455484')['Contents']
for key in list:
    os.makedirs(os.path.join("nyoo_images", os.path.dirname(key['Key'])),
                exist_ok=True)
    s3.download_file('dcb-455484', key['Key'],
                     os.path.join('nyoo_images', key['Key']))
