# YAML Configuration for Databricks
databricks:
  workspace:
    name: my-databricks-workspace
    region: us-west-2
    sku: "standard"
    managed_resource_group_id: "managed-rg"
    network:
      vpc_id: "${vpc_id}"
      subnet_ids: ["${subnet1_id}", "${subnet2_id}"]
      security_group_ids: ["${sg_id}"]
      public_subnet_name: "public-subnet"
      private_subnet_name: "private-subnet"
  outputs:
    workspace_url: ""
    workspace_id: ""
# Databricks Workspace Resource Class
import pulumi_aws as aws
from dto import DatabricksConfigDTO

class DatabricksResource:
    def __init__(self, config: DatabricksConfigDTO):
        self.config = config
        self.workspace = self.create_workspace()

    def create_workspace(self):
        workspace = aws.databricks.Workspace(
            self.config.workspace.name,
            region=self.config.workspace.region,
            sku=self.config.workspace.sku,
            managed_resource_group_id=self.config.workspace.managed_resource_group_id,
            network=self.config.workspace.network
        )

        # Capturing outputs
        self.config.outputs['workspace_url'] = workspace.url
        self.config.outputs['workspace_id'] = workspace.id

        return workspace

    def output_dto(self) -> DatabricksConfigDTO:
        return self.config
