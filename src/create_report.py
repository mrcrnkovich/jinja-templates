"""
Creates a report

    Should allow for threading in main.py module

    No Return value
"""
import logging
from pdfkit import from_string
from report import Report


def create_report(
        env, report: Report, output_path, pdf_base_config
):
    """
    Create a report
    """
    template = env.get_template(report.template_name)

    html = template.render(
        name="Template Report",
        report=report.name,
        data=report.data,
    )

    if report.to_html:
        with open(f"{output_path}/{report}.html", "w", encoding="UTF-8") as file:
            file.write(html)
    else:
        print(html)

    if report.to_pdf:
        from_string(html, f"{output_path}/{report}.pdf", options=pdf_base_config)
