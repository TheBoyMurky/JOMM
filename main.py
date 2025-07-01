import boto3
import json
import ec2

from botocore.config import Config

with open('config.json', 'r') as file:
    ec2_config_json = json.load(file)


ec2_config = Config(
    region_name = ec2_config_json['region']
)

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=ec2_config_json['access_key'],
    aws_secret_access_key=ec2_config_json['secret_key'],
    config=ec2_config
)

ec2.checar_instancia(ec2_client, ec2_config_json['ec2_id'])