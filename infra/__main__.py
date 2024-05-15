'''Walking skeleton code

import pulumi
from pulumi_aws_native import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket("my-bucket")

# Export the name of the bucket
pulumi.export("bucket_name", bucket.id)

# To test out the CICD process, I'm adding a second bucket
# Create an AWS resource (S3 Bucket)
bucket2 = s3.Bucket("my-bucket-2")

# Export the name of the bucket
pulumi.export("bucket_name", bucket2.id)
'''

'''
AWS all-in-one databricks deployment
'''
import pulumi
from dto import ConfigDTO
import yaml
import os

# Import resource classes
from resources.iam import IAMResource

# Load configuration based on the current Pulumi stack
stack = pulumi.get_stack()
config_path = f'config/{stack}.yml'

with open(config_path, 'r') as file:
    config_data = yaml.safe_load(file)

# Create DTOs from configuration
config_dto = ConfigDTO.from_dict(config_data)

# Instantiate resources with DTO
iam_resource = IAMResource(config_dto.iam)

pulumi.export('iam_outputs', iam_resource.output_dto().outputs)
