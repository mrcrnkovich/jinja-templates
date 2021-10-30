#! /usr/local/bin/python3

import pdfkit
import jinja2
import requests
import sys
import yaml
from functools import partial


pdf_options = {
    'encoding':    'UTF-8'
}

def trim(path):
    return path.strip('./').strip('.py')

def pdf_filename(report, output_dir='output'):
    return output_dir+'/'+report+'.pdf'

def get_data(path):
    return requests.get(path).json()

def main():
    # set up environment
    env = jinja2.Environment(
            loader=jinja2.PackageLoader("src"),
            autoescape=jinja2.select_autoescape()
    )

    # Should pull config from yaml file
    base_url = 'http://localhost:3000/'
    

    report = trim(sys.argv[1])
    template_name = report + '.html'
    report_url = base_url + report

    temp = env.get_template(template_name)
    html = temp.render(name = "mike",
            report=report,
            data=get_data(report_url))
    pdfkit.from_string(html, pdf_filename(report), options=pdf_options)

if __name__ == "__main__":
    main()
