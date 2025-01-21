from aws_cdk import App


def test_cdk():
    from std_utils.aws_utils.cdk.stacks.pipeline import Pipeline

    Pipeline(App(), 'Pipeline', 'connection_arn', 'repo', 'branch', [])
