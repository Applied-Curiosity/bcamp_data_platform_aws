#%%
import pulumi
import yaml
from dto import ConfigDTO
from resources.iam import IAMResource

print("Starting Pulumi script...")

#%%
# Load configuration based on the current Pulumi stack
stack = 'dev'
config_path = f'config/{stack}.yml'
print(f"Using configuration file: {config_path}")

#%%
with open(config_path, 'r') as file:
    config_data = yaml.safe_load(file)

print("Configuration data loaded:")
print(config_data)

#%%
# Create DTOs from configuration
config_dto = ConfigDTO.from_dict(config_data)
print("DTO created from configuration:")

#%%
# Instantiate IAMResource with DTO
iam_resource = IAMResource(config_dto.iam)
print("IAM Resource instantiated.")

#%%
# Export the outputs managed by the IAMResource class
output_dto = iam_resource.output_dto()
for key, value in output_dto.outputs.items():
    pulumi.export(key, value)
print("Pulumi script completed.")

# %%
