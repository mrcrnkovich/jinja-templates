#! /usr/local/bin/python3

"""
Currently the main module that runs everything.
Need to refactor.
"""

import argparse
import os
import sys
import logging
import subprocess
import jinja2
from yaml import safe_load
from create_report import create_report


def dir_exists(path):
    """
    Checks whether a directory exists.
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
    """Add cli args to argpase return results"""

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
    # Load Application Config from file
    try:
        with open(config_path, "r", encoding="UTF-8") as file:
            config = safe_load(file)
    except FileNotFoundError as err:
        logging.fatal("No Config File Found, %s", err)
        sys.exit()
    return config


def main():
    """Runs Main"""

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

    create_report(
        env=env,
        output_path=output_path,
        reports_path=reports_path,
        report=args.report,
        print_to_pdf=args.pdf,
        print_to_html=args.html,
        pdf_base_config=config.get("pdf"),
    )


if __name__ == "__main__":
    main()
