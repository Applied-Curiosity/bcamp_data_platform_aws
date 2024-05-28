import pulumi_databricks as databricks
from dto import DatabricksConfigDTO

class DatabricksResource:
    def __init__(self, config: DatabricksConfigDTO):
        self.config = config
        self.workspace = self.create_workspace()

    def create_workspace(self):
        workspace = databricks.Workspace(
            self.config.workspace['name'],
            region=self.config.workspace['region'],
            sku=self.config.workspace['sku'],
            managed_resource_group_id=self.config.workspace['managed_resource_group_id'],
            network=self.config.workspace['network']
        )

        # Capturing outputs
        self.config.outputs['workspace_url'] = workspace.url
        self.config.outputs['workspace_id'] = workspace.id

        return workspace

    def output_dto(self) -> DatabricksConfigDTO:
        return self.config