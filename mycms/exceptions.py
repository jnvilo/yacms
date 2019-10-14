from django.core.exceptions import ObjectDoesNotExist

class NodeDoesNotExist(ObjectDoesNotExist):
    pass

class PageDoesNotExist(Exception):
    pass

