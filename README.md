# Jinja Wrapper to compile documents

## About

This Jinja wrapper designed to compile static reports, documents, or even be
used as a static HTML generator. It was originally conceived as a way to
generate PDF reports from command line script by using HTML for the template.

Report layouts are basic HTML, CSS, and Javascript. The report configurations
are setup in a YAML configuration file. In the YAML file you define the
end-points where data should be retrieved.

## Options
`--print-to-pdf: Prints the report to output/[report-name].pdf`
 This is dependent on wkhtmltopdf being installed on your system
`--stdin: read data from standard in. Used with --template`
`--template: define a template to be used, do not look in the config.yml file`

## Usage

### config.yml

Define API endpoint

For each model define:
    1. Jinja template name (inside template folder)
    2. Data: API endpoint or SQL query
    3. Other meta-data
    
### TO DO:
    1. Improve Logging
    2. Include Error Handling
    3. Write Py-Tests
    4. Move methods out of Main, so the module can be imported and used in other Python programs
