from django.core.exceptions import ObjectDoesNotExist

class NodeDoesNotExist(ObjectDoesNotExist):
    pass
class CMSFieldDoesNotExist(ObjectDoesNotExist):
    pass

class PageDoesNotExist(Exception):
    pass

class CMSFieldError(Exception):
    pass
