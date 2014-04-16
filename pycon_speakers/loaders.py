import re
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, Identity, Compose
from w3lib.html import remove_tags, unquote_markup
from .items import Speaker


def _cleanup_name(name):
    """Cleanup extras in names

    >>> _cleanup_name(u'Collin Winter bio')
    u'Collin Winter'
    >>> _cleanup_name(u'Collin Winter (Google / Unladen Shallow) bio')
    u'Collin Winter'
    >>> _cleanup_name(u'Collin Winter (Google / Unladen Shallow)')
    u'Collin Winter'
    >>> _cleanup_name(u'Jim Fulton / Zope Corporation')
    u'Jim Fulton'
    >>> _cleanup_name(u'Ivan Krstic / Harvard University (presently..)')
    u'Ivan Krstic'
    """
    name = name.replace('\t', ' ')
    name = _STRIPRE1.sub(u'', name, re.I)
    return _STRIPRE2.sub(u'', name, re.I)

_STRIPRE1 = re.compile(ur'\s*(\(.*\))?( bio)?( -)?( \.)?$', re.DOTALL)
_STRIPRE2 = re.compile(ur'\s*(/.+)$', re.DOTALL)


class SpeakerLoader(ItemLoader):
    default_item_class = Speaker
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()

    image_urls_out = Identity()
    name_out = Compose(Join(), _cleanup_name)
