# YAML Configuration for Monitoring
monitoring:
  cloudtrail:
    name: myapp-trail
    s3_bucket_name: myapp-log-bucket
    include_global_service_events: true
    is_multi_region_trail: true
    enable_log_file_validation: true
  cloudwatch:
    log_group_name: myapp-log-group
    retention_in_days: 90
  outputs:
    trail_arn: ""
    log_group_arn: ""

# resources/monitoring.py
import pulumi_aws as aws
from dto import MonitoringConfigDTO

class MonitoringResource:
    def __init__(self, config: MonitoringConfigDTO):
        self.config = config
        self.setup_cloudtrail()
        self.setup_cloudwatch()

    def setup_cloudtrail(self):
        trail = aws.cloudtrail.Trail(
            self.config.cloudtrail.name,
            s3_bucket_name=self.config.cloudtrail.s3_bucket_name,
            include_global_service_events=self.config.cloudtrail.include_global_service_events,
            is_multi_region_trail=self.config.cloudtrail.is_multi_region_trail,
            enable_log_file_validation=self.config.cloudtrail.enable_log_file_validation
        )
        self.config.outputs['trail_arn'] = trail.arn

    def setup_cloudwatch(self):
        log_group = aws.cloudwatch.LogGroup(
            self.config.cloudwatch.log_group_name,
            retention_in_days=self.config.cloudwatch.retention_in_days
        )
        self.config.outputs['log_group_arn'] = log_group.arn

    def output_dto(self) -> MonitoringConfigDTO:
        return self.config
