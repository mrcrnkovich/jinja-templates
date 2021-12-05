#! /usr/local/bin/python3

import logging
import jinja2
from sys import argv
from yaml import safe_load
from pdfkit import from_string


def pdf_filename(report: str, output_dir: str = './output') -> str:
    return output_dir+'/'+report+'.pdf'


def get_data(path: str) -> dict:
    '''Takes https path and returns results in a dict'''
    from requests import get
    result = get(path)
    return result.json() if result.status_code == '200' else raise AttributeError


def main():
    logging.basicConfig(filename="./app.log", level=logging.INFO)

    report = argv[1].strip('./').strip('.py')
    logging.info(f'opening file {report}')

    config_filepath = './config.yml'
    with open(config_filepath, 'r') as f:
        config = safe_load(f)

    template_config = config.get('Templates').get(report)
    template_name = template_config.get('template_loc')
    report_url = template_config.get('end_point')

    # set up Jinja environment
    env = jinja2.Environment(
            loader=jinja2.PackageLoader("src"),
            autoescape=jinja2.select_autoescape()
    )
    template = env.get_template(template_name)
    html = template.render(name="mike",
            report=report,
            data=get_data(report_url))

    # Render to PDF
    from_string(html,
            pdf_filename(report),
            options=config.get('PDF'))


if __name__ == "__main__":
    main()
