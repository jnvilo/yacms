FROM fedora:latest

RUN yum -y install libtiff-devel libjpeg-devel libzip-devel freetype-devel \
    lcms2-devel libwebp-devel tcl-devel tk-devel python3-devel git zlib \
    openssl-devel zlib-devel 


WORKDIR /srv/mycms

ADD mycms /srv/mycms/mycms
ADD requirements.txt /srv/mycms/requirements.txt

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8002
CMD ["python3", "mycms/demo_app/manage.py", "runserver", "0.0.0.0:8002"]
