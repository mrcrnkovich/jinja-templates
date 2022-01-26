CC='pipenv run python3'

output_dir = ./src/output/
cwd = $(shell pwd)

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) \
	   	| sort \
	   	| awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

activate:
	@(. venv/bin/activate)

venv:
	@python -m venv venv

install:
	. venv/bin/activate && pip install -r requirements.txt

build:  ## Build docker image
	sudo docker build -t jinja-templates .

docker-run: build ## Run application in docker with reports, templates, logs, and output located in src
	sudo docker run --rm -v $(cwd)/src:/var/opt -v $(cwd)/src:/var/log/app jinja-templates

initial: venv activate install ## Set up initial environment

clean:	## empy the output folder
	rm -rf $(output_dir)/*

%: ## Create report.. by report name 
	@cd src && python3 app.py --dev --html $@
