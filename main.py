#! /usr/local/bin/python3

import pdfkit
import jinja2
import requests
import sys
from yaml import safe_load

config_filepath = './config.yml'

def trim(path):
    return path.strip('./').strip('.py')

def pdf_filename(report, output_dir='output'):
    return output_dir+'/'+report+'.pdf'

def get_data(path):
    return requests.get(path).json()

def main():
    
    # Load commandline args
    report = trim(sys.argv[1])

    
    # Load template configurations
    with open (config_filepath, 'r') as f:
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
    html = template.render(name = "mike",
            report=report,
            data=get_data(report_url))

    # Render to PDF
    pdfkit.from_string(html,
            pdf_filename(report),
            options=config.get('PDF'))

if __name__ == "__main__":
    main()
