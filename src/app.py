#! /usr/local/bin/python3

""" Currently the main module that runs everything.
"""

import argparse
import os
import sys
import logging
import subprocess
import jinja2
from yaml import safe_load
from create_report import create_report
from report import Report


def dir_exists(path):
    """ Checks whether a directory exists.
        If directory is not found, create the directory.
    """

    if not os.path.exists(path):
        os.mkdir(path)
    return path


def check_dependencies():
    """ Check for required non-python dependencies. """

    if subprocess.call(["which", "wkhtmltopdf"], stdout=subprocess.DEVNULL) != 0:
        logging.critical("WKHTMLTOPDF not found, can not print to PDF")
        status = True
    else:
        logging.info("System Check: WKHTMLTOPDF Found")
        status = False
    return status

def cli_arguments():
    """ Add cli arguments to argpase
        return arguments passed at runtime
    """

    arg_parser = argparse.ArgumentParser(
        description="A static report generator based on Jinja"
    )

    arg_parser.add_argument("report", help="specify which report to run")
    arg_parser.add_argument(
        "--dev", help="run reports, logs, output in dev mode", action="store_true"
    )
    arg_parser.add_argument(
        "--pdf", help="print a pdf to output_path", action="store_true"
    )
    arg_parser.add_argument(
        "--html", help="print html to output_path", action="store_true"
    )
    return arg_parser.parse_args()


def app_config(config_path):
    """ Load Application Config from file """

    try:
        with open(config_path, "r", encoding="UTF-8") as file:
            config = safe_load(file)
    except FileNotFoundError as err:
        logging.fatal("No Config File Found, %s", err)
        sys.exit()
    return config


def main():
    """
        --dev: runs all user generated content and logs in the current folder.
                Otherwise, all user generated content is located at /var/opt/
                and logs are located at /var/log/app

        Refactor report generation to allow for Threading
    """

    args = cli_arguments()
    config_path = "../config.yml"
    config = app_config(config_path)

    if args.dev:
        log_path = dir_exists("./logs")
        output_path = dir_exists("./output")
        reports_path = dir_exists("./reports")
        templates_path = dir_exists("./templates")
    else:
        log_path = dir_exists("/var/log/app/")
        output_path = dir_exists("/var/opt/output")
        reports_path = dir_exists("/var/opt/reports")
        templates_path = dir_exists("/var/opt/templates")

    logging.basicConfig(filename=f"{log_path}/app.log", level=logging.INFO)
    check_dependencies()

    logging.info("opening file %s", args.report)
    logging.info("pdf output is %s", args.pdf)

    # set up Jinja environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_path),
        autoescape=jinja2.select_autoescape(),
    )

    report = Report(
        name=args.report,
        report_path=reports_path,
        template_path = templates_path,
        to_pdf=args.pdf,
        to_html=args.html
    )
    print(args.report)
    create_report(
        env=env,
        output_path=output_path,
        report=report,
        pdf_base_config=config.get("pdf"),
    )


if __name__ == "__main__":
    main()
