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
build: init
	poetry install && \
	mkdir -p ../build && \
	poetry run zappa package dev -o ../build/${lambda_output_filename}

