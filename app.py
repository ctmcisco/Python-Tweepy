#!/usr/bin/env python3

from aws_cdk import core

from ts_tues_lambda.ts_tues_lambda_stack import TsTuesLambdaStack


app = core.App()
TsTuesLambdaStack(app, "ts-tues-lambda")

app.synth()
