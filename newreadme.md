# bcamp_data_platform_aws

BCAMP and Applied Curiosity's Data Platform Infrastructure

## AWS Walking Skeleton

As we continue to expand our skills in cloud architecture and infrastructure management, I'd like to challenge you to develop a similar setup for AWS that we've successfully implemented for Azure. Here's a structured approach to guide your research and documentation:

1. **Create a New Git Repository:**
   Begin by creating a new repository specifically for our AWS infrastructure. This will be the central place for all related code and documentation. **_I’ve already created a GitHub repo for AWS titled, `bcamp_data_platform_aws`_**
2. **Install Pulumi and AWS CLI:**
   I created a new branch off main (ghaws) for my Codespace work environment.
   I installed pulumi using the following code: curl -fsSL https://get.pulumi.com | sh
   I installed AWS CLI using codes:
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
3. **Configure AWS CLI:**
   Configure the AWS CLI with appropriate credentials. This involves setting up AWS access keys and configuring your local environment to interact with your AWS account. **_If there is a OpenID option similar to Azure, let’s try to use that._**
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

# Shawn's Notes

I'm walking through the basic set up with the documentation to see how far this will get me. I'll take step-by-step notes here, so I can revise them for our README later.

Here's the goals for this session:

- Setting up and configuring Pulumi to access your AWS account.
- Creating a new Pulumi project.
- Provisioning a new AWS S3 bucket.
- Adding an index.html file to the bucket and serving it as a static website.
- Cleaning up your deployment by destroying the resources you've provisioned.

Let's go throgh the prereqs first:

### Install Pulumi

Pulumi should be installed if you're using the `.devcontainer` in this repository. If not, install it on your local system. [Install Pulumi](https://www.pulumi.com/docs/clouds/aws/get-started/begin/#install-pulumi)

```
curl -fsSL https://get.pulumi.com | sh
```

And test it

```
pulumi version
```

### Intall Python

Again, this `.devcontainer` includes Python, Pip, and a bunch of other tools, but if you need to do it on your own, I suggest you install it from the VSCODE extension library. And remember, when creating your virtual environment, if you create it from the command line, which Pulumi will do for you if you choose to scaffold a project, you will need to set your environment through VSCODE's command pallet.
[Basically, how it's done here](https://code.visualstudio.com/docs/python/environments#_create-a-conda-environment-in-the-terminal)

If you need to perform a local install, this should help you. [Local Python Install](https://www.pulumi.com/docs/clouds/aws/get-started/begin/#install-language-runtime)

### [Configure Pulumi to Access your AWS Account](https://www.pulumi.com/docs/clouds/aws/get-started/begin/#configure-pulumi-to-access-your-aws-account)

I did have a slight scare when I realized that AWS and GCP do not have a provider as part of their Native client, the way that Azure does. No worries, though, there is a way to set up both with Pulumi, we just may need to jump through a few additional hoops.

[Databricks set up on AWS](https://www.pulumi.com/registry/packages/databricks/api-docs/mwsworkspaces/#creating-a-databricks-on-aws-workspace) We are currently focusing our efforts on the Databricks managed VPC, instead of the customer provided VPC (that will be a future implementation). We will do this for all 3 environments. This will mean that the elements we're creating in addition to Databricks are the Storage Account and the Key Vault, as well as the IAM requirements.

[Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**_At some point in the future, we will make this part of the `.devcontainer`._**

## AWS CLI Setup Instructions

Follow these steps to configure your AWS CLI:

1. **Get your AWS Access Key ID and Secret Access Key**

   - Sign in to the AWS Management Console and open the IAM console at https://console.aws.amazon.com/iam/.
   - In the navigation pane, choose Users and then choose Add user.
   - For User name, type a name for the new user. This is the name they'll use to sign in to AWS.
   - Select the check box next to Programmatic access.
   - Choose Next: Permissions.
   - On the Set permissions page, choose Attach existing policies directly.
   - In the policy list, select the check box for `AdministratorAccess`. Then choose Next: Tags.
   - Choose Next: Review to see the user details and permissions.
   - Choose Create user.
   - To view the new access key pair, choose Show. You will not have access to the secret access key again after this dialog box closes.
   - To download the key pair, choose Download .csv file. Store the keys in a secure location.

2. **Configure your AWS CLI**

   - Open your terminal.
   - Run `aws configure`.
   - You will be prompted to provide your AWS Access Key ID, AWS Secret Access Key, Default region name, and Default output format. Enter your details and press enter after each one.

3. **Test your AWS CLI configuration**

   - Run `aws s3 ls` in your terminal. If your AWS CLI is properly configured, you should see a list of your S3 buckets.

Remember, never share your AWS Access Key ID and Secret Access Key with anyone, and avoid committing them in your code or uploading them to public repositories.

## A New Pulumi Project

When starting fresh, the easiest way to align the AWS local authentication, the Pulumi authentication, and the overall workflow is to create a new Pulumi project.

For our project I used the scaffolding option:

```
pulumi new --name bcamp_data_platform_aws
```

This create a new project in Pulumi and started me down the path of creating the project. Not that I emptied the `infra` folder and changed directory to it.

Pulumi then walked me through each step including a description of the project, the template I wanted to use (I chose the aws-native-python), the AWS region we want to deploy to `east-us-1`, and finally the stack name, which I chose `dev`.

After the project was created, I was able to perform `pulumi up` and use the `display` option to see that the `my-bucket` resource. So I went ahead and let it do the deployment.

### Some additional thoughts for developers

As a devloper using this environment, you shouldn't need to install any additional tools. They are all included in the `.devcontainer.json` file and Docker file.

However, you will need to configure your own AWS cli authentication. This involves created a `.env' file in the root directory that includes the values for your authentication for AWS.

```
AWS_ACCESS_KEY_ID=<>
AWS_SECRET_ACCESS_KEY=<>
PULUMI_TOKEN=<>
```

Replace the <> with your values, the Pulumi value is optional.
