from aws_cdk import (
    core,
    aws_apigateway,
    aws_lambda,
    aws_dynamodb,
)

ZAPPA_LAMBDA_PACKAGE = "build/lambda_output.zip"
DYNAMO_TABLE_NAME = "SOME_TABLE"


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

        # create dynamo table
        dynamo_table = aws_dynamodb.Table(
            scope=self,
            id="DemoTable",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

        # Wire up the table and the function
        dynamo_table.grant_read_write_data(handler)
        handler.add_environment("DYNAMO_TABLE_NAME", dynamo_table.table_name)

        # define the apigateway
        api = aws_apigateway.LambdaRestApi(
            scope=self,
            id="API",
            handler=handler
        )
