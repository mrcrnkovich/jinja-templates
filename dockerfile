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
    pip install -r requirements.txt

WORKDIR src
CMD ls /var/opt/reports | xargs -n 1 basename -s .yml | xargs -n 1 python app.py --html --pdf
