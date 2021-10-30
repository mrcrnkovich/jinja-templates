CC=python3

template_dir = ./make_pdf/templates
templates = $(shell ls $(template_dir))
output_dir = ./output

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

clean:	## empy the output folder
	rm -rf $(output_dir)/*.pdf


%: ## where the magic happens
	$(CC) main.py $@

all: invest capital #make all reports
	open output/invest.pdf $(output_dir)/capital.pdf
