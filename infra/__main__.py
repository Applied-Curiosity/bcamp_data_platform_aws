"""An AWS Python Pulumi program"""

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
