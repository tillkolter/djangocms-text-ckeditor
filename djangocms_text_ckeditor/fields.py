# -*- coding: utf-8 -*-
from django.contrib.admin import widgets as admin_widgets
from django.db import models
from django.forms.fields import CharField
from django.utils.safestring import mark_safe
from django.utils.six import add_metaclass

from .compat import LTE_DJANGO_1_7
from .html import clean_html
from .widgets import TextEditorWidget

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^djangocms_text_ckeditor\.fields\.HTMLField'])
except ImportError:
    pass


class HTMLFormField(CharField):

    widget = TextEditorWidget

    def __init__(self, *args, **kwargs):
        conf = kwargs.pop('configuration', None)

        if conf:
            widget = TextEditorWidget(configuration=conf)
        else:
            widget = None
        kwargs.setdefault('widget', widget)
        super(HTMLFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(HTMLFormField, self).clean(value)
        return clean_html(value, full=False)


class HTMLField(models.TextField):

    def __init__(self, *args, **kwargs):
        # This allows widget configuration customization
        # from the model definition
        self.configuration = kwargs.pop('configuration', None)
        super(HTMLField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return mark_safe(value)

    def to_python(self, value):
        # On Django >= 1.8 a new method
        # was introduced (from_db_value) which is called
        # whenever the value is loaded from the db.
        # And to_python is called for serialization and cleaning.
        # This means we don't need to add mark_safe on Django >= 1.8
        # because it's handled by (from_db_value)
        if value is None:
            return value

        if LTE_DJANGO_1_7:
            # could be that value is already marked safe
            # this is ok because mark_safe is idempotent
            value = mark_safe(value)
        return value

    def formfield(self, **kwargs):
        if self.configuration:
            widget = TextEditorWidget(configuration=self.configuration)
        else:
            widget = TextEditorWidget

        defaults = {
            'form_class': HTMLFormField,
            'widget': widget,
        }
        defaults.update(kwargs)

        # override the admin widget
        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = widget
        return super(HTMLField, self).formfield(**defaults)

    def clean(self, value, model_instance):
        value = super(HTMLField, self).clean(value, model_instance)
        return clean_html(value, full=False)

if LTE_DJANGO_1_7:
    HTMLField = add_metaclass(models.SubfieldBase)(HTMLField)
