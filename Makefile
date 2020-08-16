.PHONY: build
REGISTRY_URL=hub.lnxsystems.com
PROJECT=library
IMAGE_NAME=mycms-demo-website
TAG=$(shell cat VERSION.txt)

.PHONY: build  all

all:  build tag 

build:
	docker build -t ${REGISTRY_URL}/${PROJECT}/${IMAGE_NAME}:${TAG} .

pull:   
	docker  pull ${REGISTRY_URL}/${PROJECT}/${IMAGE_NAME}:latest 

tag: 
	docker tag ${REGISTRY_URL}/${PROJECT}/${IMAGE_NAME}:${TAG} ${REGISTRY_URL}/${PROJECT}/${IMAGE_NAME}:latest
 
push:  build
	docker push ${REGISTRY_URL}/${PROJECT}/${IMAGE_NAME}:latest
	docker push ${REGISTRY_URL}/${PROJECT}/${IMAGE_NAME}:${TAG}

.PHONY: dev
dev: 	tango-icon-themes

.PHONY: tango-icon-themes
tango-icon-themes: 
	if [[ ! -d "tango-icon-themes" ]];then git clone git@github.com:jnvilo/tango-icon-themes.git;fi
