#!/usr/bin/env python3

from aws_cdk import core

from cdk_gitbot.cdk_gitbot_stack import CdkGitbotStack


app = core.App()
CdkGitbotStack(app, "cdk-gitbot")

app.synth()
