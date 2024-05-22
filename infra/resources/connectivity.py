# YAML Configuration for Connectivity
connectivity:
  vpc_peering:
    - peering_name: "vpc-peering-1"
      source_vpc_id: "${source_vpc_id}"
      target_vpc_id: "${target_vpc_id}"
      auto_accept: true
  transit_gateway:
    - gateway_name: "main-transit-gateway"
      description: "Central hub for network traffic"
      default_route_table_association: "enable"
      default_route_table_propagation: "enable"
      auto_accept_shared_attachments: "enable"
  outputs:
    peering_connection_ids: []
    transit_gateway_ids: []

# resources/connectivity.py
import pulumi_aws as aws
from dto import ConnectivityConfigDTO

class ConnectivityResource:
    def __init__(self, config: ConnectivityConfigDTO):
        self.config = config
        self.setup_vpc_peering()
        self.setup_transit_gateway()

    def setup_vpc_peering(self):
        for peer in self.config.vpc_peering:
            peering_connection = aws.ec2.VpcPeeringConnection(
                peer.peering_name,
                vpc_id=peer.source_vpc_id,
                peer_vpc_id=peer.target_vpc_id,
                auto_accept=peer.auto_accept
            )
            # Store output
            self.config.outputs['peering_connection_ids'].append(peering_connection.id)

    def setup_transit_gateway(self):
        for gateway in self.config.transit_gateway:
            transit_gateway = aws.ec2transitgateway.TransitGateway(
                gateway.gateway_name,
                description=gateway.description,
                auto_accept_shared_attachments=gateway.auto_accept_shared_attachments,
                default_route_table_association=gateway.default_route_table_association,
                default_route_table_propagation=gateway.default_route_table_propagation
            )
            # Store output
            self.config.outputs['transit_gateway_ids'].append(transit_gateway.id)

    def output_dto(self) -> ConnectivityConfigDTO:
        return self.config
