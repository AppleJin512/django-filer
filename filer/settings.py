#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.storage import get_storage_class
from filer.utils.loader import load_object
from filer.utils.recursive_dictionary import RecursiveDictionaryWithExcludes
import os
import urlparse

FILER_ENABLE_PERMISSIONS = getattr(settings, 'FILER_ENABLE_PERMISSIONS', False)

FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = getattr(settings, 'FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS', False)

FILER_PAGINATE_BY = getattr(settings, 'FILER_PAGINATE_BY', 20)

FILER_SUBJECT_LOCATION_IMAGE_DEBUG = getattr(settings, 'FILER_SUBJECT_LOCATION_IMAGE_DEBUG', False)

FILER_IS_PUBLIC_DEFAULT = getattr(settings, 'FILER_IS_PUBLIC_DEFAULT', True)

FILER_STATICMEDIA_PREFIX = getattr(settings, 'FILER_STATICMEDIA_PREFIX', None)
if not FILER_STATICMEDIA_PREFIX:
    FILER_STATICMEDIA_PREFIX = (getattr(settings, 'STATIC_URL', None) or settings.MEDIA_URL) + 'filer/'

FILER_ADMIN_ICON_SIZES = getattr(settings,"FILER_ADMIN_ICON_SIZES",(
        '16', '32', '48', '64',
))

# This is an ordered iterable that describes a list of 
# classes that I should check for when adding files
FILER_FILE_MODELS = getattr(settings, 'FILER_FILE_MODELS',
    (
        'filer.models.imagemodels.Image',
        'filer.models.filemodels.File',
    )
)

MINIMAL_FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': None,
            'OPTIONS': {},
            'UPLOAD_TO': None,
            },
        'thumbnails': {
            'ENGINE': None,
            'OPTIONS': {},
            }
    },
    'private': {
        'main': {
            'ENGINE': None,
            'OPTIONS': {},
            'UPLOAD_TO': None,
            },
        'thumbnails': {
            'ENGINE': None,
            'OPTIONS': {},
            },
        },
    }

DEFAULT_FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'filer/')),
                'base_url': urlparse.urljoin(settings.MEDIA_URL, 'filer/'),
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'filer_thumbnails/')),
                'base_url': urlparse.urljoin(settings.MEDIA_URL, 'filer_thumbnails/'),
            },
        }
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(settings.MEDIA_ROOT, '../smedia/filer')),
                'base_url': '/smedia/filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(settings.MEDIA_ROOT, '../smedia/filer_thumbnails')),
                'base_url': '/smedia/filer_thumbnails/',
            },
        },
    },
}


MINIMAL_FILER_SERVERS = {
    'private': {
        'main': {
            'ENGINE': None,
            'OPTIONS': {},
        },
        'thumbnails': {
            'ENGINE': None,
            'OPTIONS': {},
        },
    },
}

DEFAULT_FILER_SERVERS = {
    'private': {
        'main': {
            'ENGINE': 'filer.server.backends.default.DefaultServer',
            'OPTIONS': {},
        },
        'thumbnails': {
            'ENGINE': 'filer.server.backends.default.DefaultServer',
            'OPTIONS': {},
        },
    },
}

FILER_STORAGES = RecursiveDictionaryWithExcludes(MINIMAL_FILER_STORAGES, rec_excluded_keys=('OPTIONS',))
FILER_STORAGES.rec_update(getattr(settings, 'FILER_STORAGES', {}))

def update_storage_settings(settings, defaults, s, t):
    if not settings[s][t]['ENGINE']:
        settings[s][t]['ENGINE'] = defaults[s][t]['ENGINE']
        settings[s][t]['OPTIONS'] = defaults[s][t]['OPTIONS']
    if t == 'main' and not settings[s][t]['UPLOAD_TO']:
        settings[s][t]['UPLOAD_TO'] = defaults[s][t]['UPLOAD_TO']
    return settings

update_storage_settings(FILER_STORAGES, DEFAULT_FILER_STORAGES, 'public', 'main')
update_storage_settings(FILER_STORAGES, DEFAULT_FILER_STORAGES, 'public', 'thumbnails')
update_storage_settings(FILER_STORAGES, DEFAULT_FILER_STORAGES, 'private', 'main')
update_storage_settings(FILER_STORAGES, DEFAULT_FILER_STORAGES, 'private', 'thumbnails')

FILER_SERVERS = RecursiveDictionaryWithExcludes(MINIMAL_FILER_SERVERS, rec_excluded_keys=('OPTIONS',))
FILER_SERVERS.rec_update(getattr(settings, 'FILER_SERVERS', {}))

def update_server_settings(settings, defaults, s, t):
    if not settings[s][t]['ENGINE']:
        settings[s][t]['ENGINE'] = defaults[s][t]['ENGINE']
        settings[s][t]['OPTIONS'] = defaults[s][t]['OPTIONS']
    return settings

update_server_settings(FILER_SERVERS, DEFAULT_FILER_SERVERS, 'private', 'main')
update_server_settings(FILER_SERVERS, DEFAULT_FILER_SERVERS, 'private', 'thumbnails')



# Public media (media accessible without any permission checks)
FILER_PUBLICMEDIA_STORAGE = get_storage_class(FILER_STORAGES['public']['main']['ENGINE'])(**FILER_STORAGES['public']['main']['OPTIONS'])
FILER_PUBLICMEDIA_UPLOAD_TO = load_object(FILER_STORAGES['public']['main']['UPLOAD_TO'])
FILER_PUBLICMEDIA_THUMBNAIL_STORAGE = get_storage_class(FILER_STORAGES['public']['thumbnails']['ENGINE'])(**FILER_STORAGES['public']['thumbnails']['OPTIONS'])


# Private media (media accessible through permissions checks)
FILER_PRIVATEMEDIA_STORAGE = get_storage_class(FILER_STORAGES['private']['main']['ENGINE'])(**FILER_STORAGES['private']['main']['OPTIONS'])
FILER_PRIVATEMEDIA_UPLOAD_TO = load_object(FILER_STORAGES['private']['main']['UPLOAD_TO'])
FILER_PRIVATEMEDIA_THUMBNAIL_STORAGE = get_storage_class(FILER_STORAGES['private']['thumbnails']['ENGINE'])(**FILER_STORAGES['private']['thumbnails']['OPTIONS'])
FILER_PRIVATEMEDIA_SERVER = load_object(FILER_SERVERS['private']['main']['ENGINE'])(**FILER_SERVERS['private']['main']['OPTIONS'])
FILER_PRIVATEMEDIA_THUMBNAIL_SERVER = load_object(FILER_SERVERS['private']['thumbnails']['ENGINE'])(**FILER_SERVERS['private']['thumbnails']['OPTIONS'])
