# YAML Configuration for Security Settings
security:
  security_groups:
    - name: web-server-sg
      description: "Security group for web servers"
      vpc_id: "${vpc_id}"  # This will be populated dynamically
      ingress:
        - protocol: "tcp"
          from_port: 80
          to_port: 80
          cidr_blocks: ["0.0.0.0/0"]
      egress:
        - protocol: "-1"
          from_port: 0
          to_port: 0
          cidr_blocks: ["0.0.0.0/0"]
  network_acls:
    - name: web-acl
      vpc_id: "${vpc_id}"  # This will be populated dynamically
      ingress:
        - rule_number: 100
          protocol: "tcp"
          rule_action: "allow"
          cidr_block: "0.0.0.0/0"
          from_port: 80
          to_port: 80
      egress:
        - rule_number: 100
          protocol: "-1"
          rule_action: "allow"
          cidr_block: "0.0.0.0/0"
          from_port: 0
          to_port: 0
  outputs:
    security_group_ids: []
    network_acl_ids: []
