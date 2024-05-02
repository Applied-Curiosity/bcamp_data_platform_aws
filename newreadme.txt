# bcamp_data_platform_aws
BCAMP and Applied Curiosity's Data Platform Infrastructure

## AWS Walking Skeleton

As we continue to expand our skills in cloud architecture and infrastructure management, I'd like to challenge you to develop a similar setup for AWS that we've successfully implemented for Azure. Here's a structured approach to guide your research and documentation:

1. **Create a New Git Repository:**
Begin by creating a new repository specifically for our AWS infrastructure. This will be the central place for all related code and documentation. ***I’ve already created a GitHub repo for AWS titled, `bcamp_data_platform_aws`***
2. **Install Pulumi and AWS CLI:**
I created a new branch off main (ghaws) for my Codespace work environment. 
I installed pulumi using the following code: curl -fsSL https://get.pulumi.com | sh
I installed AWS CLI using codes:
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install 
3. **Configure AWS CLI:**
Configure the AWS CLI with appropriate credentials. This involves setting up AWS access keys and configuring your local environment to interact with your AWS account. ***If there is a OpenID option similar to Azure, let’s try to use that.***
4. **Set Up a Pulumi Project:**
Create a new Pulumi project in the **`infra`** directory of your repository, but this time, make sure it's configured for AWS.
First I checked my version to make sure I had the latest installed by tuping aws --version
Then I made a new directory called "infra" mkdir infra - then switched to that directory cd infra
To initilize a new Pumulmi project I ran - pulumi new aws-python
ISSUE - wants tokens?? Stop here ask questions
5. **Authenticate Pulumi with AWS:**
Instead of a service principal, you'll need to configure Pulumi to use AWS credentials. Investigate the best practices for securely managing these credentials, especially in CI/CD environments.
6. **Create GitHub Actions Workflow:**
Set up a GitHub Actions workflow that will handle the deployment of AWS resources. This should mimic the workflow we created for Azure but tailored to AWS specifics.
7. **Deploy a Minimal AWS Resource:**
As a starting point, deploy a simple AWS resource, such as an S3 bucket or an EC2 instance. Document the process and the Pulumi code used for this task.
8. **Documentation:**
For each step, provide detailed documentation on what you did, why it was done that way, and any challenges you faced. Include code snippets, command-line operations, and screenshots where applicable.

**Goal:**
The goal is not only to replicate the Azure setup but to understand the nuances of AWS and how Pulumi interacts with another cloud provider. This exercise will enhance your practical knowledge of cloud architectures and prepare you for more complex deployments.