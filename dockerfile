FROM python:3.10.1-slim

RUN apt-get -qq update -y &&\
    apt-get -qq upgrade -y &&\
    apt-get -qq install -y wkhtmltopdf vim-tiny wget unzip 


WORKDIR home

RUN wget https://github.com/mrcrnkovich/jinja-templates/archive/master.zip -q\ 
    && unzip master.zip\
    && rm -rf master.zip
RUN mv jinja-templates-master app

WORKDIR app

RUN rm -rf src/output src/reports src/logs src/templates

RUN pip install --upgrade pip &&\
    pip install jinja2 pyyaml requests pdfkit

WORKDIR src
CMD python app.py cars_phl_api --html --pdf
