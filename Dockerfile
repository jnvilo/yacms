from alpine:latest
MAINTAINER Jason Viloria <jnvilo@gmail.com> 

RUN apk update
RUN apk add --no-cache python3 \
    py3-tz \
    py3-gunicorn \
    ca-certificates \
    build-base \
    zlib-dev  \ 
    zlib \ 
    jpeg-dev \ 
    py3-pillow \ 
   python3-dev \
   freetype-dev \ 
   freetype \
   libjpeg-turbo-dev \
   libjpeg-turbo \
   tiff \
   tiff-dev \
   libwebp-dev \
   libwebp \
     
&& pip3 install -U pip

RUN mkdir /website
WORKDIR /website
ADD requirements.txt requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt;

ADD mycms mycms
ADD demo_app demo_app
ADD setup.py setup.py
ADD MANIFEST.in MANIFEST.in
ADD README.md README.md
ADD LICENSE.txt LICENSE.txt
ADD AUTHORS.txt AUTHORS.txt 
RUN python3 setup.py install  

EXPOSE 8001
WORKDIR /website/demo_app
CMD ["sh", "run.sh"]
