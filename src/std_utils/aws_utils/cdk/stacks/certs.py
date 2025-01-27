from aws_cdk import Stack
from aws_cdk.aws_certificatemanager import Certificate, CertificateValidation

from std_utils.aws_utils.cdk.models.configs import CertConfig, \
    CloudfrontCertConfig


class Certs(Stack):

    def __init__(self, config: CertConfig) -> None:
        super().__init__(config.parent, config.stack_id, env=config.env)

        self.cert = Certificate(
            self,
            config.id,
            domain_name=config.domain_name,
            validation=CertificateValidation.from_dns(config.hosted_zone)
        )


class CloudfrontCert(Certs):

    def __init__(self, config: CloudfrontCertConfig):
        super().__init__(config.cert_config)
