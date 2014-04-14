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
    """
    return _STRIPRE.sub(u'', name, re.I)
_STRIPRE = re.compile(ur'\s*(\(.*\))?( bio)?( -)?( \.)?$')


class SpeakerLoader(ItemLoader):
    default_item_class = Speaker
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()

    image_urls_out = Identity()
    name_out = Compose(Join(), _cleanup_name)
