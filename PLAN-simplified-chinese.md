# 繁简转换方案

## 目标

将 beets 管理的歌曲中的繁体中文标签（artist, album, title, albumartist, lyrics 等所有内置文本字段）全部转换为简体中文。`zhconv` 插件处理导入时的标签转换，`lyrics` 插件处理歌词转换。

## 架构设计

### 核心原则

**标签转换与歌词获取解耦**。标签转换在导入阶段独立进行，不依赖于歌词是否获取成功。

### 插件方案

使用 beets 插件系统，通过事件监听器在 `AlbumInfo`/`TrackInfo` 传递给数据库之前进行转换。

```
导入歌曲
    │
    ├── 1. Item.read()          ← 读取原始标签（保持原样）
    │
    ├── 2. lookup_candidates() ← MusicBrainz 搜索
    │       │
    │       ├── albuminfo_received 事件 → zhconv 插件转换 AlbumInfo 字段
    │       └── trackinfo_received 事件 → zhconv 插件转换 TrackInfo 字段
    │
    ├── 3. apply_metadata()     ← 转换后的数据写入数据库
    │
    ├── 4. write to DB + file   ← 存储转换后的标签
    │
    └── 5. find_lyrics()        ← lyrics 插件获取歌词并转换
            │
            ├── 获取成功 → 转换后存储
            │
            └── 获取失败 → 不存储（标签已转换）
```

### 两个独立转换点

| 转换点 | 方式 | 转换内容 |
|--------|------|----------|
| 标签转换 | `zhconv` 插件事件监听 | AlbumInfo/TrackInfo 文本字段 |
| 歌词转换 | `lyrics` 插件扩展 | lyrics 字段 |

## 实现细节

### 1. 转换函数库

**文件**: `beets/util/zhstyle.py`

使用 `opencc` 作为转换引擎。

```python
import opencc

_converter_s2t = opencc.OpenCC("s2t")
_converter_t2s = opencc.OpenCC("t2s")

def to_simplified(text: str | None) -> str | None:
    """Convert traditional Chinese to simplified Chinese."""
    if text is None:
        return None
    return _converter_t2s.convert(text)

def to_traditional(text: str | None) -> str | None:
    """Convert simplified Chinese to traditional Chinese."""
    if text is None:
        return None
    return _converter_s2t.convert(text)
```

### 2. 标签转换插件

**文件**: `beetsplug/zhconv.py`

使用 `albuminfo_received` 和 `trackinfo_received` 事件监听器。

```python
class ZhConvPlugin(BeetsPlugin):
    name = "zhconv"

    def __init__(self):
        super().__init__()
        self.config.add({
            "style": "original",  # 'original' | 'simplified' | 'traditional'
        })
        self.register_listener("albuminfo_received", self.albuminfo_received)
        self.register_listener("trackinfo_received", self.trackinfo_received)

    @property
    def converter(self):
        style = self.config["style"].get()
        if style == "simplified":
            return zhstyle.to_simplified
        elif style == "traditional":
            return zhstyle.to_traditional
        return lambda x: x  # original

    def albuminfo_received(self, info: AlbumInfo):
        # 转换 AlbumInfo 和 TrackInfo 字段...

    def trackinfo_received(self, info: TrackInfo):
        # 转换 TrackInfo 字段...
```

### 3. 歌词转换

**文件**: `beetsplug/lyrics.py`

在 `add_item_lyrics()` 中添加 `zh_style` 配置项和转换逻辑。

```python
self.config.add({
    # ... existing config ...
    "zh_style": "original",  # 'original' | 'simplified' | 'traditional'
})

# add_item_lyrics() 中
lyrics_text = new_lyrics.full_text

zh_style = self.config["zh_style"].get()
if zh_style == "simplified":
    lyrics_text = zhstyle.to_simplified(lyrics_text)
elif zh_style == "traditional":
    lyrics_text = zhstyle.to_traditional(lyrics_text)

item.lyrics = lyrics_text
```

### 4. 配置

**文件**: `beets/config_default.yaml`

```yaml
import:
    # ... existing config ...
    zh_style: original  # 'original' | 'simplified' | 'traditional'
```

## 关键代码位置

| 文件 | 说明 |
|------|------|
| `beets/util/zhstyle.py` | 繁简转换核心函数 |
| `beetsplug/zhconv.py` | 标签转换插件 |
| `beetsplug/lyrics.py` | 添加 `zh_style` 配置和歌词转换 |
| `beets/config_default.yaml` | 添加 `import.zh_style` 配置 |
| `pyproject.toml` | 添加 `opencc` 依赖 |

## 依赖

- `opencc` - 繁体/简体转换引擎

## 使用方式

```yaml
plugins: [zhconv, lyrics]

import:
    zh_style: simplified  # original | simplified | traditional

lyrics:
    zh_style: simplified  # original | simplified | traditional
```

## NOT in scope

1. 已导入数据的批量繁简转换脚本
2. 第三方插件的 flexible attributes 字段
3. 写入文件时的转换
4. 数据库 schema 变更