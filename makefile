CC=python3

template_dir = ./make_pdf/templates
templates = $(shell ls $(template_dir))

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) \
	   	| sort \
	   	| awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


templates: ## Just the templates folder
	@echo $(templates)

env:
	pip3 install pipenv
	pipenv shell

install:
	pipenv install

initial: env install

%: ## where the magic happens
	$(CC) main.py $@ \
	&& open template.pdf
