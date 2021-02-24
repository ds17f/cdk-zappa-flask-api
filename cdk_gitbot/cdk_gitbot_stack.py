from aws_cdk import (
    core,
    aws_apigateway,
    aws_lambda,
)

ZAPPA_LAMBDA_PACKAGE = "build/lambda_output.zip"


class CdkGitbotStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # define the handler function
        handler = aws_lambda.Function(
            scope=self,
            id="HandlerFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset(ZAPPA_LAMBDA_PACKAGE),
            handler="handler.lambda_handler",
            timeout=core.Duration.seconds(15)
        )

        # define the apigateway
        api = aws_apigateway.LambdaRestApi(
            scope=self,
            id="API",
            handler=handler
        )
