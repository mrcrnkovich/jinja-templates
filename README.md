# HTML/PDF Report Generator

## About

This a HTML/PDF report generator written in Python. By utilizing Jinja2
templates, it is easy to compile static reports, documents, or even be
used as a static HTML generator. It was originally conceived as a way to
generate PDF reports from command line script by using HTML for the template.

Report layouts are basic HTML, CSS, and Javascript. The report configurations,
including data sources, are setup in a YAML configuration file.

Currently, you can choose multiple data sources in the configuration, from
SQLite, Text, and API endpoints.

This project aims to fill the gap for easy to use report generators, that can
fit easily into any current workflow. Since it's a command line program, it can
be incorporated into a Airflow routine, to be run after a batch data load.


## Usage

## Options

`--print-to-pdf: Prints the report to output/[report-name].pdf`
 This is dependent on wkhtmltopdf being installed on your system
 --to-file: Prints results to file at output/[report-name]
 --stdout: Prints results to standard out. This is the default.
`--stdin: read data from standard in. Used with --template`
`--template: define a template to be used, do not look in the config.yml file`

### Default Templates
There are two default templates included
with the package:
    1. Three panes (Top , bottom_left, bottm_right)
    2. Three panes (Left, top_right, bottom_right)


### config.yml

Define API endpoint

For each model define:
    1. Jinja template name (inside template folder)
    2. Data: API endpoint or SQL query
    3. Other meta-data

## Run in Docker

A docker file is provided in the repo. Local access binding, or Docker Volumes
are available for the following directories:
    - reports:/var/opt/reports
    - ouput:/var/opt/output/
    - logs:/var/log/app
    - templates:/var/opt/templates

for example:

    `docker run -v $(pwd):/var/opt -v $(pwd):/var/log/app jinja-templates`
