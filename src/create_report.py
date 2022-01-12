"""
Creates a report


    Should allow for threading in main.py module

    No Return value
"""
import sys
import logging
from yaml import safe_load
from pdfkit import from_string
from router.data_router import handler


def create_report(
    env, print_to_pdf, print_to_html, report, reports_path, output_path, pdf_base_config
):
    """
    Create a report
    """
    # Load Report Config from file
    try:
        with open(f"{reports_path}/{report}.yml", "r", encoding="UTF-8") as file:
            report_config = safe_load(file).get("report")
    except FileNotFoundError as err:  # raise exception
        logging.fatal("No report configuration found, %s", err)
        sys.exit()

    template_name = report_config.get("template")
    report_data = handler(report_config.get("data"))
    template = env.get_template(template_name)

    html = template.render(
        name="Template Report",
        report=report_config.get("title", report),
        data=report_data,
    )

    if print_to_html:
        with open(f"{output_path}/{report}.html", "w", encoding="UTF-8") as file:
            file.write(html)
    else:
        print(html)

    if print_to_pdf:
        from_string(html, f"{output_path}/{report}.pdf", options=pdf_base_config)
