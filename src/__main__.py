#! /usr/local/bin/python3

import logging
import jinja2
from sys import argv
from yaml import safe_load
from pdfkit import from_string
from .get_data import api_data


def pdf_filename(report: str, output_dir: str = './output') -> str:
    return output_dir+'/'+report+'.pdf'

def main():
    logging.basicConfig(filename="./app.log", level=logging.INFO)
    
    print_to_pdf = argv[-1] == '--print-to-pdf'
    report = argv[1].strip('./').strip('.py')
    
    logging.info(f'opening file {report}')
    logging.info(f'output is {print_to_pdf}')

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
    data = api_data(report_url)

    html = template.render(name="mike",
            report=report,
            data=data)

    print(html)
    
    if print_to_pdf:
        from_string(html,
            pdf_filename(report),
            options=config.get('PDF'))


if __name__ == "__main__":
    main()
