from aws_cdk import App, Stack, Stage
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

from std_utils.aws_utils.cdk.utils import get_environment


class Pipeline(Stack):

    def __init__(
        self,
        scope: App,
        stack_id: str,
        connection_arn: str,
        repo: str,
        branch: str,
        stages: list[Stage]
    ):
        super().__init__(scope, stack_id, env=get_environment())
        pipeline = CodePipeline(
            self, "Pipeline", synth=ShellStep(
                "Synth",  # Use a connection created using the AWS console to
                # authenticate to GitHub
                # Other sources are available.
                input=CodePipelineSource.connection(
                    repo, branch, connection_arn=connection_arn
                ), commands=["npm ci", "npm run build", "npx cdk synth"]
            )
        )
        for stage in stages:
            pipeline.add_stage(stage)
