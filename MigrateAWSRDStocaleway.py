import boto3
from scaleway_api import Scaleway
import pymysql

# AWS credentials
aws_access_key = 'YOUR_AWS_ACCESS_KEY'
aws_secret_key = 'YOUR_AWS_SECRET_KEY'
aws_region = 'us-east-1'

# Scaleway credentials
scaleway_token = 'YOUR_SCALEWAY_TOKEN'
scaleway_organization = 'YOUR_SCALEWAY_ORGANIZATION'

# RDS details
rds_instance_identifier = 'your-aws-rds-instance-identifier'
rds_username = 'your-rds-username'
rds_password = 'your-rds-password'
rds_database_name = 'your-rds-database-name'

# Scaleway database details
scaleway_db_type = 'db-x64-2-s'
scaleway_db_version = '10'
scaleway_db_name = 'your-scaleway-database-name'
scaleway_db_username = 'your-scaleway-username'
scaleway_db_password = 'your-scaleway-password'

# Connect to AWS RDS
rds = boto3.client('rds', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

# Get AWS RDS instance details
response = rds.describe_db_instances(DBInstanceIdentifier=rds_instance_identifier)
rds_instance = response['DBInstances'][0]

# Get RDS endpoint and port
rds_endpoint = rds_instance['Endpoint']['Address']
rds_port = rds_instance['Endpoint']['Port']

# Connect to Scaleway
scw = Scaleway(token=scaleway_token, organization=scaleway_organization)

# Create a new database on Scaleway
database = scw.create_instance(commercial_type=scaleway_db_type, image='scaleway/ubuntu-focal', name=scaleway_db_name)

# Wait for Scaleway database to be ready
scw.wait_instance(database['server']['id'])

# Get Scaleway database details
scw_db = scw.get_instance(database['server']['id'])

# Print Scaleway database details
print(f'Scaleway Database ID: {scw_db["server"]["id"]}')
print(f'Scaleway Database Public IP: {scw_db["server"]["public_ip"]["address"]}')

# Transfer data from AWS RDS to Scaleway (use your preferred method, e.g., mysqldump, AWS Database Migration Service)

# Update your application configurations to use the new Scaleway database details.

# Terminate the AWS RDS instance if migration is successful
rds.delete_db_instance(DBInstanceIdentifier=rds_instance_identifier, SkipFinalSnapshot=True)
print(f'AWS RDS Instance {rds_instance_identifier} terminated.')
