#! /usr/local/bin/python3

import pdfkit
import jinja2
import requests
import sys

report_url = 'http://localhost:3000/'
filename_pdf = lambda x: x + '.pdf'

pdf_options = {
    'encoding':    'UTF-8'
}

def main():
    env = jinja2.Environment(
            loader=jinja2.PackageLoader("src"),
            autoescape=jinja2.select_autoescape()
    )

    report = sys.argv[1].strip('./').strip('.py')
    template_path = report + '.html'
    print(report, template_path)

    r_data = requests.get( report_url + report ).json()
    temp = env.get_template(template_path)
    html = temp.render(name = "mike", report=report, data=r_data)
    pdfkit.from_string(html, filename_pdf('template'), options=pdf_options)

if __name__ == "__main__":
    main()
