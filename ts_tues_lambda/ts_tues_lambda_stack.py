from aws_cdk import (
    core,
    aws_events as event,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_events_targets as targets
)


class TsTuesLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        consumer_key = self.node.try_get_context("consumer_key")
        consumer_secret = self.node.try_get_context("consumer_secret")
        access_token = self.node.try_get_context("access_token")
        access_token_secret = self.node.try_get_context("access_token_secret")
        yt_api_key = self.node.try_get_context("yt_api_key")
        youtube_channel_id = self.node.try_get_context("youtube_channel_id")

        # Lambda Role
        role = iam.Role(self, "lambda_role", 
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name="techsnips_lambda_role"
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_managed_policy_arn(self,'iam-role-attach',"arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
        )

        # create lambda function
        function = _lambda.Function(self, "lambda_function",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="lambda-handler.main",
            function_name="ts-tuesday",
            environment={
                'twit_cons_key': consumer_key,
                'twit_cons_sec': consumer_secret,
                'twit_acc_tok': access_token,
                'twit_acc_sec': access_token_secret,
                'yt_api_key': yt_api_key,
                'yt_channel': youtube_channel_id
            },
            role=role,
            code=_lambda.Code.asset("./lambda")
        )

        # Run every Tuesday
        rule = event.Rule(
            self, "Rule",
            schedule=event.Schedule.cron(
                hour='9',
                minute='45',
                week_day='TUE'    
            )
        )
        rule.add_target(targets.LambdaFunction(function))