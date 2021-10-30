#! /usr/local/bin/python3

import pdfkit
import jinja2
import requests
import sys
from yaml import safe_load
# from functools import partial

config_filepath = './config.yml'

def trim(path):
    return path.strip('./').strip('.py')

def pdf_filename(report, output_dir='output'):
    return output_dir+'/'+report+'.pdf'

def get_data(path):
    return requests.get(path).json()

def main():
    # set up Jinja environment
    env = jinja2.Environment(
            loader=jinja2.PackageLoader("src"),
            autoescape=jinja2.select_autoescape()
    )

    # Load template configurations
    with open (config_filepath, 'r') as f:
        config = safe_load(f)

    pdf_config = config['PDF']
    template_config = config['Templates']
    print(pdf_config)

    report = trim(sys.argv[1])

    template_name = config['Templates'][report]['template_loc']
    report_url = config['Templates'][report]['end_point']

    template = env.get_template(template_name)
    html = template.render(name = "mike",
            report=report,
            data=get_data(report_url))

    pdfkit.from_string(html,
            pdf_filename(report),
            options=pdf_config)

if __name__ == "__main__":
    main()
