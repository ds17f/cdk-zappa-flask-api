# cdk-gitbot
This is a `cdk` project which uses `poetry` to manage the package and environment

## Prerequisites
You'll need:
* Python >= 3.7
* nodejs >= 10.0
* `cdk` 
* `poetry`

### Install cdk
cdk is a `nodejs` app.  Even though this project is written in python you'll need a working `node` environment in order to run the `cdk` cli tool.  Setup and install of nodejs is beyond the scope of this project

Install cdk with
```
npm install -g aws-cdk
```

### Install poetry
```
pip install poetry
```

## Quickstart
The following command will:
* Build a zappa package out of the `lambda_src` package
* Run a `cdk-deploy` of that package
```
make cdk-deploy
```


## Manual Quickstart
### Initialize
You'll need to initialize and install dependencies
```
poetry install
```

### Run tests
```
poetry run python -m unittest discover
```

### Deploy
```
poetry run cdk deploy
```

## Try it out
```
curl https://itbwdxnrg8.execute-api.us-east-1.amazonaws.com/prod/
```

## Notes
* [Flask/Zappa/CDK](https://dev.to/raphael_jambalos/more-than-hello-world-in-lambda-build-and-deploy-flask-apis-in-aws-lambda-via-cdk-1m04)
* [Flask/Zappa/Apig](https://github.com/adamjq/aws-lambda-flask-proxy-api)
* [Makefiles](https://medium.com/aigent/makefiles-for-python-and-beyond-5cf28349bf05)
* [Zappa Packaging](https://github.com/zappa/Zappa#package)