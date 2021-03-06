# -*- coding: utf-8 -*-

# Copyright 2015-2019 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract manga-chapters from https://dynasty-scans.com/"""

from .common import ChapterExtractor
from .. import text
import json
import re


class DynastyscansChapterExtractor(ChapterExtractor):
    """Extractor for manga-chapters from dynasty-scans.com"""
    category = "dynastyscans"
    pattern = r"(?:https?://)?(?:www\.)?dynasty-scans\.com(/chapters/[^/?&#]+)"
    test = (
        (("http://dynasty-scans.com/chapters/"
          "hitoribocchi_no_oo_seikatsu_ch33"), {
            "url": "dce64e8c504118f1ab4135c00245ea12413896cb",
            "keyword": "1564965671ac69bb7fbc340538397f6bd0aa269b",
        }),
        (("http://dynasty-scans.com/chapters/"
          "new_game_the_spinoff_special_13"), {
            "url": "dbe5bbb74da2edcfb1832895a484e2a40bc8b538",
            "keyword": "22b35029bc65d6d95db2e2c147b0a37f2d290f29",
        }),
    )
    root = "https://dynasty-scans.com"

    def metadata(self, page):
        info  , pos = text.extract(page, "<h3 id='chapter-title'><b>", "</b>")
        author, pos = text.extract(page, " by ", "</a>", pos)
        group , pos = text.extract(page, '"icon-print"></i> ', '</span>', pos)
        date  , pos = text.extract(page, '"icon-calendar"></i> ', '<', pos)

        match = re.match(
            (r"(?:<a[^>]*>)?([^<]+)(?:</a>)?"  # manga name
             r"(?: ch(\d+)([^:<]*))?"  # chapter info
             r"(?:: (.+))?"),  # title
            info
        )

        return {
            "manga": text.unescape(match.group(1)),
            "chapter": text.parse_int(match.group(2)),
            "chapter_minor": match.group(3) or "",
            "title": text.unescape(match.group(4) or ""),
            "author": text.remove_html(author),
            "group": (text.remove_html(group) or
                      text.extract(group, ' alt="', '"')[0] or ""),
            "date": date,
            "lang": "en",
            "language": "English",
        }

    def images(self, page):
        data = text.extract(page, "var pages = ", ";\n")[0]
        return [
            (self.root + img["image"], None)
            for img in json.loads(data)
        ]
