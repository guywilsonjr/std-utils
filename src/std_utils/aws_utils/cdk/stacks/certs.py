from typing import Optional

from aws_cdk import Stack, Environment
from aws_cdk.aws_certificatemanager import (
    Certificate,
    CertificateProps
)
from constructs import Construct
from pydantic import validate_call

from std_utils.aws_utils.cdk.models.configs import CloudfrontCertConfig


class Certs(Stack):
    props: CertificateProps

    @validate_call
    def __init__(
            self,
            parent: Construct,
            construct_id: str,
            props: CertificateProps,
            env: Optional[Environment] = None
    ) -> None:
        super().__init__(parent, construct_id, env=env)

        self.cert = Certificate(
            self,
            'Cert',
            domain_name=props.domain_name,
            validation=props.validation,
            certificate_name=props.certificate_name,
            subject_alternative_names=props.subject_alternative_names,
            key_algorithm=props.key_algorithm,
            transparency_logging_enabled=props.transparency_logging_enabled
        )


class CloudfrontCert(Certs):

    def __init__(self, config: CloudfrontCertConfig):
        super().__init__(config.cert_config, )
