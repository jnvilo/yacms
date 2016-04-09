VERSION_STRING="0.0.1"

import os
import logging
import sh

logger = logging.getLogger("yacms")

from django.conf import settings
from pathlib import Path
import subprocess



#Get the YACMS_ARTICLE_LOGOS_DIR if defined in settings, otherwise
#set a default.




YACMS_BASE_URL = "cms/"
YACMS_ARTICLE_LOGOS_URL ="/static_assets/yacms/logos"


from django.conf import settings


print(settings.AUTHENTICATION_BACKENDS )


def compile_dustjs():

    """
    Compiles all templates in ./tmpl  to ./static/yacms/js/templates.js

    """

    node_modules_dir = settings.YACMS_SETTINGS["NODE_MODULES_DIR"]
    node_modules_bindir = Path(node_modules_dir, "dustjs-linked/bin")
    dustc_bin = Path(node_modules_dir, "dustjs-linkedin/bin/dustc")


    yacms_root_dir = os.path.dirname(os.path.abspath(__file__))
    yacms_dustjs_tmpl_dir = Path(yacms_root_dir, "tmpl")
    yacms_js_dir = Path(yacms_root_dir, "static/yacms/js")

    #we want to run something like: $ dustc tmpl/**/*.dust -o output.js

    cmd = "{} {}/* -o {}/yacms_dust_templates.js --pwd={}".format(dustc_bin.as_posix(), yacms_dustjs_tmpl_dir.as_posix(), yacms_js_dir.as_posix(), yacms_dustjs_tmpl_dir.as_posix())
    logger.info("Compiling dustjs templates by running: {}".format(cmd))


    output = subprocess.check_output(cmd, shell=True,   stderr=subprocess.STDOUT)
    print(output)

compile_dustjs()
