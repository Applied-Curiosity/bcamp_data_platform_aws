# [Databricks Neworking Options]

### Overview of Databricks Networking Options and Their Trade-offs

1. **Serverless Option**

   - **Description**: Databricks manages the virtual network for you.
   - **Pros**: Simplified setup and management.
   - **Cons**: Limited control over the network, which may not meet some organizations' security or compliance requirements.
   - **Dependencies**: No custom VPC configuration allowed.
   - **Requirements**: None, as the network is managed by Databricks.

2. **Customer-Managed VPC**

   - **Description**: Deploy Databricks in a VPC managed by the customer.
   - **Pros**: Full control over network settings.
   - **Cons**: Increased complexity and management overhead.
   - **Dependencies**: Requires a VPC with appropriate subnets, routing tables, and security groups.
   - **Requirements**: Configuration of VPC, subnets, security groups, and route tables.

3. **VPC Peering**

   - **Description**: Establishes a direct network connection between the Databricks VPC and other VPCs.
   - **Pros**: Secure, direct connection without public internet traversal.
   - **Cons**: Management complexity and potential VPC peering limits.
   - **Dependencies**: Requires VPC peering connections and appropriate route tables.
   - **Requirements**: VPC Peering setup, route tables updates.

4. **AWS PrivateLink**

   - **Description**: Provides private connectivity between the Databricks VPC and other AWS services.
   - **Pros**: Keeps traffic within AWS network for enhanced security.
   - **Cons**: Additional setup complexity.
   - **Dependencies**: Requires PrivateLink endpoints and VPC endpoint services.
   - **Requirements**: Setup PrivateLink endpoints, configure security groups, and route tables.

5. **Transit Gateway**

   - **Description**: Allows scalable and flexible inter-VPC routing.
   - **Pros**: Centralized control of network traffic.
   - **Cons**: Complexity in setup and management.
   - **Dependencies**: Requires a Transit Gateway and attachments.
   - **Requirements**: Setup Transit Gateway, configure VPC attachments and route tables.

6. **Virtual Private Gateway**
   - **Description**: Connects the Databricks VPC to on-premises networks using a VPN connection.
   - **Pros**: Secure communication between on-premises and cloud.
   - **Cons**: Potential latency and performance issues.
   - **Dependencies**: Requires a Virtual Private Gateway and VPN connection.
   - **Requirements**: Setup Virtual Private Gateway, configure VPN connections and route tables.

### YAML Configuration Examples

**\*Note: this are not the actual YAML we use for the IaC code, just a sample of required fields**

#### Serverless Option

```yaml
databricks:
  networking_option: "serverless"
  requirements: []
  dependencies: []
  notes: "Databricks manages the virtual network. No custom VPC configuration allowed."
```

#### Customer-Managed VPC

```yaml
databricks:
  networking_option: "customer_managed_vpc"
  requirements:
    - vpc_id: "vpc-123456"
    - subnets:
        - subnet_id: "subnet-123456"
          cidr_block: "10.0.1.0/24"
        - subnet_id: "subnet-789012"
          cidr_block: "10.0.2.0/24"
    - security_groups:
        - sg_id: "sg-123456"
  dependencies: []
  notes: "Full control over network settings. Requires VPC with appropriate subnets and security groups."
```

#### VPC Peering

```yaml
databricks:
  networking_option: "vpc_peering"
  requirements:
    - vpc_id: "vpc-123456"
    - peered_vpc_id: "vpc-789012"
    - route_tables:
        - route_table_id: "rtb-123456"
          routes:
            - destination_cidr_block: "10.0.2.0/24"
              target: "pcx-123456"
  dependencies:
    - vpc_peering_connection: "pcx-123456"
  notes: "Secure, direct connection. Requires VPC peering connections and appropriate route tables."
```

#### AWS PrivateLink

```yaml
databricks:
  networking_option: "aws_privatelink"
  requirements:
    - vpc_id: "vpc-123456"
    - subnets:
        - subnet_id: "subnet-123456"
          cidr_block: "10.0.1.0/24"
    - security_groups:
        - sg_id: "sg-123456"
    - privatelink_endpoints:
        - service_name: "com.amazonaws.us-east-1.s3"
          vpc_endpoint_id: "vpce-123456"
  dependencies: []
  notes: "Keeps traffic within AWS network. Requires PrivateLink endpoints and VPC endpoint services."
```

#### Transit Gateway

```yaml
databricks:
  networking_option: "transit_gateway"
  requirements:
    - transit_gateway_id: "tgw-123456"
    - vpc_id: "vpc-123456"
    - attachments:
        - vpc_attachment:
            vpc_id: "vpc-123456"
            subnet_ids: ["subnet-123456", "subnet-789012"]
  dependencies: []
  notes: "Centralized control of network traffic. Requires Transit Gateway and attachments."
```

#### Virtual Private Gateway

```yaml
databricks:
  networking_option: "virtual_private_gateway"
  requirements:
    - vpc_id: "vpc-123456"
    - virtual_private_gateway_id: "vgw-123456"
    - customer_gateway_id: "cgw-123456"
    - vpn_connection:
        vpn_connection_id: "vpn-123456"
        tunnel_options:
          - tunnel_inside_cidr: "169.254.1.0/30"
          - pre_shared_key: "your-pre-shared-key"
  dependencies: []
  notes: "Secure communication between on-premises and cloud. Requires Virtual Private Gateway and VPN connection."
```

### Summary

Each networking option for Databricks on AWS provides different levels of control and security, with various trade-offs:

- **Serverless**: Simplified management, but limited control.
- **Customer-Managed VPC**: Full control, but increased complexity.
- **VPC Peering**: Secure connections between VPCs, but management complexity.
- **AWS PrivateLink**: Enhanced security within AWS network, but setup complexity.
- **Transit Gateway**: Scalable, centralized control, but complex setup.
- **Virtual Private Gateway**: Secure hybrid cloud, but potential latency issues.

These configurations guide the network engineer on the required resources and settings for integrating Databricks into their network.
