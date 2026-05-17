Zhconv Plugin
=============

The ``zhconv`` plugin converts Chinese text in music tags between simplified
and traditional Chinese during import. It ensures that your music library
consistently uses your preferred Chinese script.

Currently, the plugin supports converting the following fields:

- **Album**: ``album``, ``artist``, ``albumartist``, ``albumartist_sort``,
  ``albumdisambig``, ``artist_sort``, ``releasegroupdisambig``, ``label``,
  ``genre``, ``style``, ``comments``, ``disctitle``, ``albumartist_credit``,
  ``albumartists``, ``albumartists_credit``, ``albumartists_sort``

- **Track**: ``title``, ``artist``, ``artist_sort``, ``album``, ``albumartist``,
  ``comments``, ``disctitle``, ``genre``, ``style``, ``arrangers``,
  ``composers``, ``composers_sort``, ``lyricists``, ``remixers``, ``work``,
  ``work_disambig``, ``albumartist_sort``, ``artist_credit``, ``artists``,
  ``artists_credit``, ``artists_sort``

The plugin uses `OpenCC`_ for high-quality Chinese text conversion.

.. _OpenCC: https://github.com/BYVoid/OpenCC

Install
-------

Firstly, enable ``zhconv`` plugin in your configuration (see
:ref:`using-plugins`). Then, install ``beets`` with ``lyrics`` extra which
includes the ``opencc`` dependency:

.. code-block:: bash

    pip install "beets[lyrics]"

Alternatively, install ``opencc`` directly:

.. code-block:: bash

    pip install opencc

Configuration
-------------

To configure the plugin, add a ``zhconv:`` section to your configuration file.
Default configuration:

.. code-block:: yaml

    zhconv:
        style: original

The available options are:

- **style**: The target Chinese script style. Can be:

  - ``original`` (default): Keep the original text unchanged.
  - ``simplified``: Convert traditional Chinese to simplified Chinese.
  - ``traditional``: Convert simplified Chinese to traditional Chinese.

Usage
-----

When enabled, the plugin automatically converts Chinese text during import.
No manual intervention is required.

For example, with ``style: simplified``, a track with artist name
``太陽之子`` will be stored as ``太阳之子`` in your beets library.

To convert Chinese text for existing tracks in your library, run the
``beet update`` command after changing the ``style`` setting. Note that
this will re-fetch metadata from MusicBrainz and may overwrite other tag
changes.

.. seealso::

   :doc:`lyrics` for converting lyrics between simplified and traditional
   Chinese. The lyrics plugin has its own ``zh_style`` configuration option.