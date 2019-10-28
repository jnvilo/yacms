class PageRegistry(type):

    REGISTRY = {}
    VIEWCLASS_REGISTRY = {}
    SERIALIZERCLASS_REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)

        if cls.__name__ not in ["BasePage"]:
            cls.REGISTRY[new_cls.__name__] = new_cls
            return new_cls

    @classmethod
    def sync_pagetypes_to_db(cls):
        """
        This makes sure that all the pages registered here 
        are also in the database. 
        """

        for name, klass in cls.REGISTRY.items():
            if name not in ["BasePage"]:
                cls._make_pagetype_db_entry(name, klass)

    @classmethod
    def _make_pagetype_db_entry(cls, name, klass):
        from mycms.models import PageType

        pt, c = PageType.objects.get_or_create(class_name=name)

        if c:
            "It was just created, add the defaults"
            if klass.get_display_name():
                pt.display_name = klass.get_display_name()
            else:
                pt.display_name = klass.__name__

            if klass.get_base_path():
                pt.base_path = klass.get_base_path()
            else:
                pt.base_path = "/cms"

            if klass.get_template():
                pt.template = klass.get_template()

            pt.save()

    @classmethod
    def register_default_serializers(cls):

        for name, klass in cls.REGISTRY.items():
            serializer_class = klass.build_serializer()
            cls.SERIALIZERCLASS_REGISTRY.update({name: serializer_class})

    @classmethod
    def register_api_views(self):
        pass

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)

    @classmethod
    def build_router_urls(cls, router):
        # router = routers.DefaultRouter()
        for name, klass in cls.REGISTRY.items():
            prefix = "{}".format(name.lower())
            viewset = klass.build_viewset()
            router.register(prefix, viewset, basename=name.lower())

        return router.urls

    @classmethod
    def get_serializer(cls, name):

        return cls.SERIALIZERCLASS_REGISTRY.get(name)

    @classmethod
    def get_pageclass(cls, name):
        return cls.REGISTRY.get(name)
