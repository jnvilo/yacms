VERSION_STRING="0.0.1"

import logging

logger = logging.getLogger("yacms")

from django.conf import settings



#Get the YACMS_ARTICLE_LOGOS_DIR if defined in settings, otherwise
#set a default. 

if hasattr(settings, "YACMS_ARTICLE_LOGOS_DIR"):
    YACMS_ARTICLE_LOGOS_URL = settings.YACMS_ARTICLE_LOGOS_URL
    #forcefully remove the trailing / just in case it exists
    YACMS_ARTICLE_LOGOS_URL = YACMS_ARTICLE_LOGOS_URL.rstrip("/")
else:
    YACMS_ARTICLE_LOGOS_URL = "/static/yacms/logos"

logger.debug("YACMS_ARTICLE_LOGOS_URL: {}".format(YACMS_ARTICLE_LOGOS_URL))



YACMS_BASE_URL = getattr(settings, "YACMS_PREFIX", "mycms/")


if not YACMS_BASE_URL.endswith("/"):
    YACMS_BASE_URL = YACMS_BASE_URL + "/"

if YACMS_BASE_URL.startswith("/"):
    YACMS_BASE_URL = YACMS_BASE_URL.lstrip("/")
    
YACMS_PREFIX_REGEX = "^{}".format(YACMS_BASE_URL)

logger.debug("YACMS_PREFIX: {}".format(YACMS_BASE_URL))