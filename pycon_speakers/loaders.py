import re
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, Identity, Compose
from w3lib.html import remove_tags, unquote_markup
from .items import Speaker


def _cleanup_name(name):
    return _STRIPRE.sub(u'', name, re.I)
_STRIPRE = re.compile(ur'\s*\(.*\)( bio|$)?')


class SpeakerLoader(XPathItemLoader):
    default_item_class = Speaker
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()

    image_urls_out = Identity()
    name_out = Compose(Join(), _cleanup_name)
