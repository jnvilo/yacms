import os


def ensure_user_is_created(username, email, password, superuser=False):
    """
    This is used on initial setup of MyCMS to create some default 
    accounts with default username/passwords.
    """
    from mycms.models import CMSUser
    from django.core.exceptions import ObjectDoesNotExist

    try:
        user = CMSUser.objects.get(username=username)
    except ObjectDoesNotExist as e:
        # admin_user does not exist
        if superuser:
            user = CMSUser.objects.create_superuser(username, email, password)
        else:
            user = CMSUser.objects.create_user(username, email, password)

    print("user exists")


def sanitize_path(path, parent=None):
    """
    Provide default / as path when path is empty. Make sure that 
    the path does not end with /.
    """

    if path is None:
        path = "/"
    elif not path.startswith("/"):
        if parent is None:
            parent = "/"
        path = os.path.join(parent, path)

    path = os.path.normpath(path)  # remove any trailing slash

    return path


def is_integer(value):

    if type(value) == int:
        return True

    try:
        int(value)
    except Exception as e:
        return False


def get_boolean_from_string(value):
    """
    This will return a boolean from string parameters. For example this 
    allows user to pass flag="N" for for False. 
    """

    TRUE_VALUES = {
        "t",
        "T",
        "y",
        "Y",
        "yes",
        "YES",
        "true",
        "True",
        "TRUE",
        "on",
        "On",
        "ON",
        "1",
        1,
        True,
    }
    FALSE_VALUES = {
        "f",
        "F",
        "n",
        "N",
        "no",
        "NO",
        "false",
        "False",
        "FALSE",
        "off",
        "Off",
        "OFF",
        "0",
        0,
        0.0,
        False,
    }

    if value in TRUE_VALUES:
        return True
    elif value in FALSE_VALUES:
        return False
    else:
        raise AttributeError("Value : {} could not be converted to a boolean.")
