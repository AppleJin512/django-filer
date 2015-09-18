#-*- coding: utf-8 -*-
from django.contrib.staticfiles.templatetags.staticfiles import static

from filer.settings import FILER_ADMIN_ICON_SIZES


class IconsMixin(object):
    """
    Can be used on any model that has a _icon attribute. will return a dict
    containing urls for icons of different sizes with that name.
    """
    @property
    def icons(self):
        r = {}
        if getattr(self, '_icon', False):
            for size in FILER_ADMIN_ICON_SIZES:
                r[size] = static("filer/icons/%s_%sx%s.png" % (self._icon, size, size))
        return r
