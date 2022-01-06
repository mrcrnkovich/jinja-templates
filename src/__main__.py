#! /usr/local/bin/python3

import os
import logging
import jinja2
from sys import argv
from yaml import safe_load
from pdfkit import from_string
from .helpers import api_data


def test_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def check_dependencies():
    import subprocess
    if subprocess.call(['which', 'wkhtmltopdf']) != 0:
        logging.critical("WKHTMLTOPDF not found, can not print to PDF")
    else:
        logging.info("System Check: WKHTMLTOPDF Found")

def main():
    log_base_path = test_dir("./logs")
    logging.basicConfig(filename=log_base_path+"/app.log",
                level=logging.INFO)

    check_dependencies()
    report = argv[1].strip('./').strip('.py')
    config_filepath = test_dir("./config.yml")
    output_base_path = test_dir("./output")
    pdf_filename = output_base_path + '/' + report + '.pdf'
    
    # set up command line options
    print_to_pdf = argv[-1] == '--print-to-pdf'

    logging.info(f'opening file {report}')
    logging.info(f'pdf output is {print_to_pdf}')

    if not os.path.exists(config_filepath):
        logging.fatal("No Config File Found")
    with open(config_filepath, 'r') as f:
        config = safe_load(f)

    template_config = config.get('reports').get(report)
    template_name = template_config.get('template').get('location')
    report_url = template_config.get('data').get('source')

    # set up Jinja environment
    env = jinja2.Environment(
            loader=jinja2.PackageLoader("src"),
            autoescape=jinja2.select_autoescape()
    )

    template = env.get_template(template_name)
    data = api_data(report_url)

    html = template.render(name="mike",
            report=report,
            data=data)

    print(html)
    
    if print_to_pdf:
        from_string(html,
            pdf_filename,
            options=config.get('PDF'))


if __name__ == "__main__":
    main()
