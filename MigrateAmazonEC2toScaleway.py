import boto3
from scaleway_api import Scaleway

# AWS credentials
aws_access_key = 'YOUR_AWS_ACCESS_KEY'
aws_secret_key = 'YOUR_AWS_SECRET_KEY'
aws_region = 'us-east-1'

# Scaleway credentials
scaleway_token = 'YOUR_SCALEWAY_TOKEN'
scaleway_organization = 'YOUR_SCALEWAY_ORGANIZATION'

# EC2 instance details
instance_id = 'i-xxxxxxxxxxxxxxxxx'  # Replace with your EC2 instance ID
instance_type = 'DEV1-S'  # Replace with desired Scaleway instance type
ami_id = 'scaleway/ubuntu-focal'  # Replace with desired Scaleway AMI ID

# Connect to AWS and get instance details
ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
response = ec2.describe_instances(InstanceIds=[instance_id])
instance = response['Reservations'][0]['Instances'][0]
private_ip = instance['PrivateIpAddress']
key_name = instance['KeyName']

# Connect to Scaleway
scw = Scaleway(token=scaleway_token, organization=scaleway_organization)

# Create a new instance on Scaleway
server = scw.create_server(commercial_type=instance_type, image=ami_id, name=f'Migrated_Instance_{instance_id}')

# Wait for Scaleway instance to be ready
scw.wait_server(server['server']['id'])

# Get Scaleway server details
scw_server = scw.get_server(server['server']['id'])

# Print Scaleway server details
print(f'Scaleway Server ID: {scw_server["server"]["id"]}')
print(f'Scaleway Public IP: {scw_server["server"]["public_ip"]["address"]}')

# Additional steps for data transfer and configuration updates may be required based on your specific use case.
# For example, you may need to transfer data from S3 to Scaleway Object Storage, update DNS records, etc.

# Update your application configurations to use the new Scaleway server details.

# Terminate the AWS EC2 instance if migration is successful
ec2.terminate_instances(InstanceIds=[instance_id])
print(f'AWS EC2 Instance {instance_id} terminated.')
