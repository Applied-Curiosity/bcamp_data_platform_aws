import pulumi
import pulumi_aws as aws
import pulumi_databricks as databricks
import pulumi_random as random

# Configuration
config = pulumi.Config()
aws_region = config.require("awsRegion")
databricks_account_id = config.require("databricksAccountId")
cross_account_arn = config.require("crossAccountArn")
root_bucket_name = config.require("rootBucketName")
key_arn = config.require("keyArn")

# VPC setup
vpc = aws.ec2.Vpc("vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={"Name": "databricks-vpc"}
)

# Subnets
public_subnet1 = aws.ec2.Subnet("public_subnet1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone=f"{aws_region}a",
    map_public_ip_on_launch=True,
    tags={"Name": "public-subnet-1"}
)

public_subnet2 = aws.ec2.Subnet("public_subnet2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone=f"{aws_region}b",
    map_public_ip_on_launch=True,
    tags={"Name": "public-subnet-2"}
)

public_subnet3 = aws.ec2.Subnet("public_subnet3",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    availability_zone=f"{aws_region}c",
    map_public_ip_on_launch=True,
    tags={"Name": "public-subnet-3"}
)

private_subnet1 = aws.ec2.Subnet("private_subnet1",
    vpc_id=vpc.id,
    cidr_block="10.0.4.0/24",
    availability_zone=f"{aws_region}a",
    tags={"Name": "private-subnet-1"}
)

private_subnet2 = aws.ec2.Subnet("private_subnet2",
    vpc_id=vpc.id,
    cidr_block="10.0.5.0/24",
    availability_zone=f"{aws_region}b",
    tags={"Name": "private-subnet-2"}
)

private_subnet3 = aws.ec2.Subnet("private_subnet3",
    vpc_id=vpc.id,
    cidr_block="10.0.6.0/24",
    availability_zone=f"{aws_region}c",
    tags={"Name": "private-subnet-3"}
)

# Internet Gateway
igw = aws.ec2.InternetGateway("igw",
    vpc_id=vpc.id,
    tags={"Name": "databricks-igw"}
)

# NAT Gateway
eip = aws.ec2.Eip("eip",
    vpc=True,
    tags={"Name": "databricks-eip"}
)

nat_gateway = aws.ec2.NatGateway("nat_gateway",
    allocation_id=eip.id,
    subnet_id=public_subnet1.id,
    tags={"Name": "databricks-nat-gateway"}
)

# Route Tables
public_route_table = aws.ec2.RouteTable("public_route_table",
    vpc_id=vpc.id,
    routes=[{
        "cidr_block": "0.0.0.0/0",
        "gateway_id": igw.id
    }],
    tags={"Name": "public-route-table"}
)

private_route_table = aws.ec2.RouteTable("private_route_table",
    vpc_id=vpc.id,
    routes=[{
        "cidr_block": "0.0.0.0/0",
        "nat_gateway_id": nat_gateway.id
    }],
    tags={"Name": "private-route-table"}
)

# Associate Route Tables
aws.ec2.RouteTableAssociation("public_route_table_association1",
    subnet_id=public_subnet1.id,
    route_table_id=public_route_table.id
)

aws.ec2.RouteTableAssociation("public_route_table_association2",
    subnet_id=public_subnet2.id,
    route_table_id=public_route_table.id
)

aws.ec2.RouteTableAssociation("public_route_table_association3",
    subnet_id=public_subnet3.id,
    route_table_id=public_route_table.id
)

aws.ec2.RouteTableAssociation("private_route_table_association1",
    subnet_id=private_subnet1.id,
    route_table_id=private_route_table.id
)

aws.ec2.RouteTableAssociation("private_route_table_association2",
    subnet_id=private_subnet2.id,
    route_table_id=private_route_table.id
)

aws.ec2.RouteTableAssociation("private_route_table_association3",
    subnet_id=private_subnet3.id,
    route_table_id=private_route_table.id
)

# Security Group
security_group = aws.ec2.SecurityGroup("security_group",
    vpc_id=vpc.id,
    description="Allow all inbound traffic",
    ingress=[{
        "protocol": "-1",
        "from_port": 0,
        "to_port": 0,
        "cidr_blocks": ["0.0.0.0/0"]
    }],
    egress=[{
        "protocol": "-1",
        "from_port": 0,
        "to_port": 0,
        "cidr_blocks": ["0.0.0.0/0"]
    }],
    tags={"Name": "databricks-sg"}
)

# S3 Bucket
s3_bucket = aws.s3.Bucket("s3_bucket",
    bucket=root_bucket_name,
    acl="private",
    tags={"Name": "databricks-root-bucket"}
)

# IAM Role for Cross-Account
assume_role_policy = databricks.get_aws_assume_role_policy(external_id=databricks_account_id).json

cross_account_role = aws.iam.Role("cross_account_role",
    assume_role_policy=assume_role_policy,
    tags={"Name": "databricks-cross-account-role"}
)

cross_account_role_policy = aws.iam.RolePolicy("cross_account_role_policy",
    role=cross_account_role.id,
    policy=databricks.get_aws_cross_account_policy().json
)

# Databricks Workspace
mws_credentials = databricks.MwsCredentials("mws_credentials",
    account_id=databricks_account_id,
    credentials_name="databricks-creds",
    role_arn=cross_account_role.arn
)

mws_storage_configuration = databricks.MwsStorageConfigurations("mws_storage_configuration",
    account_id=databricks_account_id,
    storage_configuration_name="databricks-storage",
    bucket_name=s3_bucket.id
)

mws_networks = databricks.MwsNetworks("mws_networks",
    account_id=databricks_account_id,
    network_name="databricks-network",
    vpc_id=vpc.id,
    subnet_ids=[private_subnet1.id, private_subnet2.id, private_subnet3.id],
    security_group_ids=[security_group.id]
)

databricks_workspace = databricks.MwsWorkspaces("databricks_workspace",
    account_id=databricks_account_id,
    workspace_name="databricks-workspace",
    aws_region=aws_region,
    credentials_id=mws_credentials.credentials_id,
    storage_configuration_id=mws_storage_configuration.storage_configuration_id,
    network_id=mws_networks.network_id,
    token=databricks.MwsWorkspacesTokenArgs(),
    custom_tags={
        "Environment": "Production"
    }
)

# Outputs
pulumi.export("databricksWorkspaceUrl", databricks_workspace.workspace_url)
pulumi.export("s3BucketName", s3_bucket.id)
