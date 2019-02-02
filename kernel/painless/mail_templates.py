from django.template import loader
from django.conf import settings


import os

BASE_DIR = settings.BASE_DIR

def get_html_message(template, request, context):
    
    if template.endswith('.html') or template.endswith('.htm'):
        file_name = BASE_DIR + '/media/templates/mail/' + template    
    else:
        raise ValueError("template is not valid")
    
    return loader.render_to_string(file_name, context)