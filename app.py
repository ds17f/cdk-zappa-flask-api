#!/usr/bin/env python3

from aws_cdk import core

from cdk_slackbot.cdk_slackbot_stack import CdkSlackbotStack


app = core.App()
CdkSlackbotStack(app, "cdk-slackbot")

app.synth()
