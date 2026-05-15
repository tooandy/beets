# TODOs - dev/chinese-lyrics-sources

## Pending Tasks

- [ ] 在 `beet import` 导入过程中，将繁体中文自动转换为简体中文
  - 需要在自动匹配标签时处理 `Artist`, `Album`, `Title` 等字段中的繁简差异
  - 可以使用 `opencc` 或 `zhconv` 库进行转换
  - 参考 MusicBrainz 返回的繁简差异（如 `太阳之子` vs `太陽之子`）

- [ ] 中文歌词使用大模型判断是否是原唱歌词
  - 当搜索结果中有多个版本时（翻唱、Live版等），需要判断哪个是原唱
  - 可以利用 AI/LLM 分析歌词内容来判断是否为原版歌词

- [ ] 中文歌词可以将繁体中文转换为简体中文
  - 或者可以统一将所有歌曲中繁体中文标签值都转换为简体中文
  - 需要设计何时触发转换比较合适（例如：导入时/匹配时/保存时）

- [ ] 使用 QQ Music 和网易云音乐获取专辑封面
  - 目前歌词源已实现，可以扩展获取 album artwork
  - QQ Music 和 NetEase 都提供专辑封面 URL

- [ ] 歌词搜索时标题匹配问题（繁体 vs 简体）
  - 目前 `_title_matches` 方法无法匹配繁简不同的标题（如 `太陽之子` vs `太阳之子`）
  - 需要在搜索前将查询和结果都转换为同一字体进行匹配
  - 或者在搜索时就进行繁简转换后再匹配

## Completed

- [x] 添加 QQ Music 歌词源
- [x] 添加网易云音乐歌词源
- [x] 修复 NetEase 搜索时加入 album 参数提高匹配准确性
- [x] 为 QQMusic 和 NetEase 添加调试日志
- [x] QQMusic 搜索时加入 album 参数（与 NetEase 保持一致）