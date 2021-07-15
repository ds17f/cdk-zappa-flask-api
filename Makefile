git_hash=$(shell git rev-parse --verify --short HEAD)
local_version=$(shell git diff --quiet || echo -local)
build_tag=$(git_hash)$(local_version)
release_tag=dev0
lambda_output_filename=lambda_output.zip #lambda_output_${build_tag}.zip

# api_image_name=cloudformer-api
# sync_image_name=cloudformer-sync
# deploy_image_name=cloudformer-deploy

.PHONY: init
init:
	poetry install
	poetry env info

.PHONY: build-lamdba
build-lambda:
	$(MAKE) -C ./lambda_src build

.PHONY: cdk-diff
cdk-diff: init build-lambda
	poetry run cdk diff

.PHONY: cdk-bootstrap
cdk-bootstrap: init
	poetry run cdk bootstrap


.PHONY: cdk-deploy
cdk-deploy: init cdk-bootstrap build-lambda
	poetry run cdk deploy --require-approval never


.PHONY: clean
clean: clean-pycache
	rm ${lambda_output_filename}
	rm -rf build
#	rm -rf cloudformer_api.egg-info
#	rm -rf dist
#	rm -f MANIFEST
#	rm -f .coverage
#	rm -f coverage.xml
#	rm -f junit.xml
#	rm -f report.xml
#	rm -f .pytest.cache
	
.PHONY: clean-pycache
clean-pycache:
	find . -depth -name __pycache__ -exec rm -rf {} \;
	find . -depth -name '*.pyc' -exec rm -rf {} \;

#
# .PHONY: test
# test: lint cfn-lint unittest
# 
# .PHONY: lint
# lint: flake8 pylint
# 
# .PHONY: cfn-lint
# cfn-lint:
# 	sh -c "find src/cloudformer_lib -name \*.yml | xargs poetry run cfn-lint -i W3005,E3002,E2510,E2505,E2004,W2509,E3003,W1001 -t"
# 
# .PHONY: unittest
# unittest:
# 	poetry run pytest -vv --junitxml=report.xml --cov-config .coveragerc --verbose --cov-report term --cov-report xml:coverage.xml --cov=src/cloudformer_api --cov=src/cloudformer_lib tests/ --ignore=src/cloudformer_lib/scripts
# 
# .PHONY: flake8
# flake8:
# 	poetry run flake8 --max-complexity 20 src/cloudformer_api src/cloudformer_lib scripts/deploy
# 
# .PHONY: pylint
# pylint:
# 	poetry run pylint src/cloudformer_api src/cloudformer_lib tests scripts/deploy
# 
 
 
# .PHONY: docker-build
# docker-build: docker-build-api docker-build-sync-task docker-build-deploy-task
# 
# .PHONY: docker-build-api
# docker-build-api: poetry.lock
# 	docker build --build-arg ARTIFACTORY_USERNAME=${ARTIFACTORY_USERNAME} --build-arg ARTIFACTORY_PASSWORD=${ARTIFACTORY_PASSWORD} --build-arg BUILD_TAG=$(build_tag) --build-arg RELEASE_TAG=$(release_tag) -t $(api_image_name):$(build_tag) -t $(api_image_name):latest .
# 
# .PHONY: docker-build-sync-task
# docker-build-sync-task: poetry.lock
# 	docker build --file Dockerfile.sync-task --build-arg ARTIFACTORY_USERNAME=${ARTIFACTORY_USERNAME} --build-arg ARTIFACTORY_PASSWORD=${ARTIFACTORY_PASSWORD} --build-arg BUILD_TAG=$(build_tag) --build-arg RELEASE_TAG=$(release_tag) -t $(sync_image_name):$(build_tag) -t $(sync_image_name):latest .
# 
# .PHONY: docker-build-deploy-task
# docker-build-deploy-task: poetry.lock
# 	docker build --file Dockerfile.deploy-task --build-arg ARTIFACTORY_USERNAME=${ARTIFACTORY_USERNAME} --build-arg ARTIFACTORY_PASSWORD=${ARTIFACTORY_PASSWORD} --build-arg BUILD_TAG=$(build_tag) --build-arg RELEASE_TAG=$(release_tag) -t $(deploy_image_name):$(build_tag) -t $(deploy_image_name):latest .
# 
# .PHONY: run-docker-devenv
# run-docker-devenv:
# 	cd docker-dev-env; \
# 	docker-compose run --rm --service-ports shell
# 
# .PHONY: run-docker-api
# run-docker-api:
# 	cd docker-dev-env; \
# 	docker-compose run --rm --service-ports cloudformer-api
# 
# .PHONY: build-docker-devenv
# build-docker-devenv:
# 	cd docker-dev-env; \
# 	[ -z "${ARTIFACTORY_PASSWORD}" ] && echo "ERROR: Please set the env variable ARTIFACTORY_PASSWORD" && exit 1; \
# 	docker-compose build --build-arg ARTIFACTORY_PASSWORD=${ARTIFACTORY_PASSWORD} shell
# 
# .PHONY: integration
# integration:
# 	poetry run pytest -x --verbose integration_tests/integration_test.py
# 
# .PHONY: integration-deployall
# integration-deployall:
# 	poetry run pytest -x --verbose integration_tests/integration_test_deployall.py
