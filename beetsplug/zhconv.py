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
        style = config["zh_style"].get()
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

        # Album-level fields (scalar strings)
        self.convert_field(info, "album")
        self.convert_field(info, "artist")
        self.convert_field(info, "artist_credit")
        self.convert_field(info, "artist_sort")
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
        self.convert_field(info, "script")

        # Album-level fields (lists)
        self.convert_field(info, "artists")
        self.convert_field(info, "artists_credit")
        self.convert_field(info, "artists_sort")
        self.convert_field(info, "genres")
        self.convert_field(info, "albumtypes")

        # Track-level fields inside AlbumInfo.tracks
        for track in info.tracks:
            self.convert_track_info(track)

    def trackinfo_received(self, info: TrackInfo):
        """Convert TrackInfo fields to the target Chinese style (singleton import)."""
        self.convert_track_info(info)

    def convert_track_info(self, track: TrackInfo):
        """Convert all Chinese text fields in a TrackInfo object."""
        convert = self.converter

        # Scalar string fields
        self.convert_field(track, "title")
        self.convert_field(track, "artist")
        self.convert_field(track, "artist_credit")
        self.convert_field(track, "artist_sort")
        self.convert_field(track, "album")
        self.convert_field(track, "disctitle")
        self.convert_field(track, "work")
        self.convert_field(track, "work_disambig")
        self.convert_field(track, "composer_sort")

        # List fields
        self.convert_field(track, "artists")
        self.convert_field(track, "artists_credit")
        self.convert_field(track, "artists_sort")
        self.convert_field(track, "arrangers")
        self.convert_field(track, "composers")
        self.convert_field(track, "composers_ids")
        self.convert_field(track, "lyricists")
        self.convert_field(track, "lyricists_ids")
        self.convert_field(track, "remixers")
        self.convert_field(track, "remixers_ids")
        self.convert_field(track, "arrangers_ids")