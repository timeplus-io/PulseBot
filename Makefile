# PulseBot Docker Makefile
# Build and push Docker images to Docker Hub

# Variables
IMAGE_NAME := pulsebot
IMAGE_TAG ?= 0.1.0
DOCKER_REPO := timeplus
FULL_IMAGE_NAME := $(DOCKER_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

# Default registry (Docker Hub)
REGISTRY := docker.io

# Multi-platform support
PLATFORMS ?= linux/amd64,linux/arm64
SINGLE_PLATFORM ?= linux/amd64

# Docker build arguments
DOCKER_BUILD_ARGS ?=

# Help target
.PHONY: help
help:
	@echo "PulseBot Docker Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  build            Build Docker image locally (single platform)"
	@echo "  build-multi      Build Docker image for multiple platforms"
	@echo "  tag              Tag the image for Docker Hub"
	@echo "  push             Push image to Docker Hub"
	@echo "  build-push       Build and push image to Docker Hub (single platform)"
	@echo "  build-push-multi Build and push multi-platform image to Docker Hub"
	@echo "  clean            Remove local Docker image"
	@echo ""
	@echo "Variables:"
	@echo "  IMAGE_TAG        Docker image tag (default: 0.1.0)"
	@echo "  DOCKER_REPO      Docker Hub repository (default: timeplus)"
	@echo "  PLATFORMS        Platforms for multi-platform build (default: linux/amd64,linux/arm64)"
	@echo "  SINGLE_PLATFORM  Platform for single platform build (default: linux/amd64)"
	@echo "  DOCKER_BUILD_ARGS Additional docker build arguments"

# Build the Docker image (single platform)
.PHONY: build
build:
	docker build --platform=$(SINGLE_PLATFORM) $(DOCKER_BUILD_ARGS) -t $(IMAGE_NAME):$(IMAGE_TAG) .

# Build the Docker image (multi-platform)
.PHONY: build-multi
build-multi:
	docker buildx build --platform=$(PLATFORMS) $(DOCKER_BUILD_ARGS) -t $(IMAGE_NAME):$(IMAGE_TAG) .

# Tag the image for Docker Hub
.PHONY: tag
tag:
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(FULL_IMAGE_NAME)

# Push the image to Docker Hub (single platform)
.PHONY: push
push:
	docker push $(FULL_IMAGE_NAME)

# Build and push the image to Docker Hub (single platform)
.PHONY: build-push
build-push: build tag push

# Build and push the image to Docker Hub (multi-platform)
.PHONY: build-push-multi
build-push-multi: buildx-setup
	docker buildx build --platform=$(PLATFORMS) $(DOCKER_BUILD_ARGS) -t $(FULL_IMAGE_NAME) --push .

# Setup Docker buildx builder
.PHONY: buildx-setup
buildx-setup:
	docker buildx create --name pulsebot-builder --use 2>/dev/null || docker buildx use pulsebot-builder

# Remove local Docker image
.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true
	docker rmi $(FULL_IMAGE_NAME) || true

# Login to Docker Hub (optional target)
.PHONY: login
login:
	docker login

# Display image information
.PHONY: info
info:
	@echo "Image Name: $(IMAGE_NAME)"
	@echo "Image Tag: $(IMAGE_TAG)"
	@echo "Docker Repository: $(DOCKER_REPO)"
	@echo "Full Image Name: $(FULL_IMAGE_NAME)"
	@echo "Registry: $(REGISTRY)"
	@echo "Single Platform: $(SINGLE_PLATFORM)"
	@echo "Multi Platforms: $(PLATFORMS)"