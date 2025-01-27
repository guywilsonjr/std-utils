from functools import cached_property
from typing import Any
from std_utils.aws_utils.cdk.models import interface_overrides

from aws_cdk import App, Environment, Stack, Stage
from aws_cdk.aws_route53 import IHostedZone
from constructs import Construct
from pydantic import BaseModel, ConfigDict, Field

from std_utils.aws_utils.utils import AWSRegion
from std_utils.models.git import GithubRepositoryBranch


class ConstructConfig(BaseModel):
    """
    Model that represents the configuration for the CDK stack.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    parent: Construct
    id: str
    env: Environment


class CDKStackConfig(ConstructConfig):

    @cached_property
    def stack_id(self) -> str:
        return self.id


class CDKAppStackConfig(CDKStackConfig):
    parent: App

    @cached_property
    def stack_id(self) -> str:
        return self.id


class CDKNestedStackConfig(CDKStackConfig):
    parent: Stack


class CertConfig(ConstructConfig):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    hosted_zone: IHostedZone
    domain_name: str
    cert_region: AWSRegion
    cert_id: str = 'Cert'


class CloudfrontCertConfig(CertConfig):
    """
    Model that represents the configuration for the certificate.
    """
    id: str = 'CloudfrontCert'
    cert_region: AWSRegion = AWSRegion.US_EAST_1

    @cached_property
    def cert_config(self):
        return CertConfig(
            parent=self.parent,
            id=self.id,
            env=self.env,
            hosted_zone=self.hosted_zone,
            domain_name=self.domain_name,
            cert_region=self.cert_region
        )


class CertStackConfig(CDKNestedStackConfig):
    """
        Model that represents the configuration for the certificate.
        """
    id: str = 'Certs'
    cert_configs: list[CertConfig]


class PipelineStageConfig(BaseModel):
    stage_class: type[Stage]
    stage_class_kwargs: dict[str, Any]


class PipelineConfig(CDKAppStackConfig):
    parent: App
    connection_arn: str
    repository_branch: GithubRepositoryBranch
    trigger_on_push: bool = True
    self_mutation: bool = True
    docker_enabled: bool = True
    stage_configs: list[PipelineStageConfig] = Field(min_length=1)

    @cached_property
    def docker_enabled_for_self_mutation(self) -> bool:
        return self.self_mutation and self.docker_enabled
