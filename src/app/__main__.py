#! /usr/local/bin/python3
""" Currently the main module that runs everything.
    Need to refactor.
"""

import argparse
import os
import sys
import logging
import subprocess
import jinja2
from yaml import safe_load
from pdfkit import from_string
from data import handler


def dir_exists(path):
    """Checks whether a directory exists.
    If directory is not found, create the directory.
    """
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def check_dependencies():
    """Check for required non-python dependencies."""

    if subprocess.call(["which", "wkhtmltopdf"], stdout=subprocess.DEVNULL) != 0:
        logging.critical("WKHTMLTOPDF not found, can not print to PDF")
    else:
        logging.info("System Check: WKHTMLTOPDF Found")


def cli_arguments():
    """Add cli args to argpase:
    return results
    """
    arg_parser = argparse.ArgumentParser(
        description="A static report generator based on Jinja"
    )

    arg_parser.add_argument("report", help="specify which report to run")
    arg_parser.add_argument(
        "--pdf", help="print a pdf to output_path", action="store_true"
    )
    arg_parser.add_argument(
        "--html", help="print html to output_path", action="store_true"
    )
    return arg_parser.parse_args()


def main():
    """Runs Main"""
    logging.basicConfig(filename=f"{dir_exists('../logs')}/app.log", level=logging.INFO)

    check_dependencies()
    args = cli_arguments()

    config_path = "../../config.yml"
    output_path = dir_exists("../output")
    reports_path = dir_exists("../reports")
    templates_path = dir_exists("../templates")

    # set up command line options

    logging.info("opening file %s", args.report)
    logging.info("pdf output is %s", args.pdf)

    # Load Application Config from file
    try:
        with open(config_path, "r", encoding="UTF-8") as file:
            config = safe_load(file)
    except:
        logging.fatal("No Config File Found")
        sys.exit()

    # Load Report Config from file
    try:
        with open(f"{reports_path}/{args.report}.yml", "r", encoding="UTF-8") as file:
            report_config = safe_load(file).get("report")
    except:  # raise exception
        logging.fatal("No report configuration found")
        sys.exit()

    # set up Jinja environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_path),
        autoescape=jinja2.select_autoescape(),
    )

    template_name = report_config.get("template")
    report_data = handler.handler(report_config.get("data"))
    template = env.get_template(template_name)

    html = template.render(
        name="mike", report=report_config.get("title", args.report), data=report_data
    )

    if args.html:
        with open(f"{output_path}/{args.report}.html", "w", encoding="UTF-8") as file:
            file.write(html)
    else:
        print(html)

    if args.pdf:
        from_string(html, f"{output_path}/{args.report}.pdf", options=config.get("pdf"))


if __name__ == "__main__":
    main()
