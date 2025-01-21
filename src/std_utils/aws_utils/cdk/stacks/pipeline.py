from aws_cdk import Stack
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

from std_utils.aws_utils.models import PipelineConfig


class Pipeline(Stack):
    _default_synth_commands = ["npm ci", "npm run build", "npx cdk synth"]

    def __init__(self, config: PipelineConfig):
        super().__init__(config.parent, config.stack_id, env=config.env)
        repo_string = f'{config.repository_branch.repo.owner}/{config.repository_branch.repo.name}'
        pipeline = CodePipeline(
            self,
            "Pipeline",
            docker_enabled_for_self_mutation=config.docker_enabled_for_self_mutation,
            docker_enabled_for_synth=config.docker_enabled,
            self_mutation=config.self_mutation,
            publish_assets_in_parallel=True,
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.connection(
                    trigger_on_push=config.trigger_on_push,
                    repo_string=repo_string,
                    repository_branch=config.repository_branch.repo_branch,
                    connection_arn=config.connection_arn
                ),
                commands=self._default_synth_commands
            )
        )
        for stage in config.stages:
            pipeline.add_stage(stage)
