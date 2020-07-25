FROM hub.lnxsystems.com/library/python:centos8-1

ENV DBNAME /app/data/db.sqlite3

RUN mkdir -p /app/data && mkdir /app/mycms
COPY mycms /app/mycms/mycms
COPY demo_website /app/mycms/demo_website
COPY entrypoint.sh /app/mycms/entrypoint.sh 
COPY LICENSE.txt /app/mycms/LICENSE.txt
COPY setup.py /app/mycms/setup.py
COPY setup.cfg /app/mycms/setup.cfg
copy AUTHORS.txt /app/mycms/AUTHORS.txt
COPY README.md /app/mycms/README.md
COPY requirements.txt /app/mycms/requirements.txt
COPY MANIFEST.in /app/mycms/MANIFEST.in
WORKDIR /app/mycms/
RUN python3.8 setup.py install 

WORKDIR /app/mycms/demo_website
ENTRYPOINT ["/app/mycms/demo_website/rundev.sh"] 
#ENTRYPOINT ["/bin/bash"]

