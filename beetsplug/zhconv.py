"""Convert Chinese text between simplified and traditional Chinese."""

from __future__ import annotations

import logging

from beets import config
from beets.autotag.hooks import AlbumInfo, TrackInfo
from beets.plugins import BeetsPlugin

from beets.util import zhstyle

log = logging.getLogger("beets")


class ZhConvPlugin(BeetsPlugin):
    """Convert Chinese text to simplified or traditional Chinese during import."""

    name = "zhconv"

    def __init__(self):
        super().__init__()

        # Register event listeners
        self.register_listener("albuminfo_received", self.albuminfo_received)
        self.register_listener("trackinfo_received", self.trackinfo_received)

    @property
    def converter(self):
        """Return the appropriate conversion function based on config."""
        style = config["import"]["zh_style"].get()
        if style == "simplified":
            return zhstyle.to_simplified
        elif style == "traditional":
            return zhstyle.to_traditional
        return lambda x: x  # original — no conversion

    def convert_value(self, value):
        """Convert a value (string or list of strings) to target Chinese style."""
        if isinstance(value, str):
            return self.converter(value)
        elif isinstance(value, list):
            return [self.converter(v) if isinstance(v, str) else v for v in value]
        return value

    def convert_field(self, info, field: str):
        """Convert a single field on an info object if it exists and is a string/list."""
        value = getattr(info, field, None)
        if value is not None:
            setattr(info, field, self.convert_value(value))

    def albuminfo_received(self, info: AlbumInfo):
        """Convert AlbumInfo fields to the target Chinese style."""
        convert = self.converter

        # Album-level fields (AlbumInfo.__init__ params)
        self.convert_field(info, "album")
        self.convert_field(info, "artist")
        self.convert_field(info, "label")
        self.convert_field(info, "genre")
        self.convert_field(info, "style")
        self.convert_field(info, "comments")
        self.convert_field(info, "disctitle")
        self.convert_field(info, "albumdisambig")
        self.convert_field(info, "releasegroupdisambig")
        self.convert_field(info, "release_group_title")
        self.convert_field(info, "catalognum")
        self.convert_field(info, "country")

        # Track-level fields inside AlbumInfo.tracks
        for track in info.tracks:
            track.title = convert(track.title) if isinstance(track.title, str) else track.title
            track.artist = convert(track.artist) if isinstance(track.artist, str) else track.artist
            track.disctitle = convert(track.disctitle) if isinstance(track.disctitle, str) else track.disctitle
            track.arrangers = self.convert_value(track.arrangers)
            track.composers = self.convert_value(track.composers)
            track.composer_sort = self.convert_value(track.composer_sort)
            track.lyricists = self.convert_value(track.lyricists)
            track.remixers = self.convert_value(track.remixers)
            track.work = convert(track.work) if isinstance(track.work, str) else track.work
            track.work_disambig = convert(track.work_disambig) if isinstance(track.work_disambig, str) else track.work_disambig

    def trackinfo_received(self, info: TrackInfo):
        """Convert TrackInfo fields to the target Chinese style (singleton import)."""
        convert = self.converter
        self.convert_field(info, "title")
        self.convert_field(info, "disctitle")
        self.convert_field(info, "arrangers")
        self.convert_field(info, "composers")
        self.convert_field(info, "composer_sort")
        self.convert_field(info, "lyricists")
        self.convert_field(info, "remixers")
        self.convert_field(info, "work")
        self.convert_field(info, "work_disambig")