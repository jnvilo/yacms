from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import os
from . settings import BASE_DIR


class TemplateSampleLoader(View):

    def get(self, request, **kwargs):

        template_name = kwargs.get("template", None)

        if template_name:
            return render(request, "bootstrap_templates/{}".format(template_name))
        else:
            #Return a list of html files in bootstrap_templates

            bootstrap_examples_dir = os.path.join(BASE_DIR, "templates/bootstrap_templates")

            files = []
            for filename in os.listdir(path=bootstrap_examples_dir):
                if filename.endswith(".html"):
                    files.append(filename)

            return render(request, "bootstrap_templates.html", { "files": files})


