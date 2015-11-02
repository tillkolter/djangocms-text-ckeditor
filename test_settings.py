# -*- coding: utf-8 -*-
from tempfile import mkdtemp

gettext = lambda s: s

HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'djangocms_picture',
        'djangocms_link',
    ],
    'LANGUAGE_CODE': 'en',
    'LANGUAGES': (
        ('en', gettext('English')),
        ('fr', gettext('French')),
        ('it', gettext('Italiano')),
    ),
    'CMS_LANGUAGES': {
        1: [
            {
                'code': 'en',
                'name': gettext('English'),
                'public': True,
            },
            {
                'code': 'it',
                'name': gettext('Italiano'),
                'public': True,
            },
            {
                'code': 'fr',
                'name': gettext('French'),
                'public': True,
            },
        ],
        'default': {
            'hide_untranslated': False,
        },
    },
    'MIGRATION_MODULES': {
        'djangocms_picture': 'djangocms_picture.migrations_django',
    },
    'CMS_PERMISSION': True,
    'CMS_PLACEHOLDER_CONF': {
        'content': {
            'plugins': ['TextPlugin', 'PicturePlugin'],
            'text_only_plugins': ['LinkPlugin'],
            'extra_context': {'width': 640},
            'name': gettext('Content'),
            'language_fallback': True,
            'default_plugins': [
                {
                    'plugin_type': 'TextPlugin',
                    'values': {
                        'body': '<p>Lorem ipsum dolor sit amet...</p>',
                    },
                },
            ],
            'child_classes': {
                'TextPlugin': ['PicturePlugin', 'LinkPlugin'],
            },
            'parent_classes': {
                'LinkPlugin': ['TextPlugin'],
            },
            'plugin_modules': {
                'LinkPlugin': 'Extra',
            },
            'plugin_labels': {
                'LinkPlugin': 'Add a link',
            }
        },
    },
    'FILE_UPLOAD_TEMP_DIR': mkdtemp(),
    'SITE_ID': 1
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_text_ckeditor')

if __name__ == '__main__':
    run()
