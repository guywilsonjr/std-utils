from typing import runtime_checkable, Protocol

from aws_cdk import aws_route53


@runtime_checkable
class IHostedZone(aws_route53.IHostedZone, Protocol):
    pass


aws_route53.IHostedZone = IHostedZone
