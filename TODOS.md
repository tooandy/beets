# TODOs - beets Chinese support

## Pending Tasks

### 1. 大模型能力增强 (LLM Enhancement)

使用大模型增强 beets 中文功能：

- [ ] **原唱歌词判断**
  - 当搜索结果中有多个版本时（翻唱、Live版等），需要判断哪个是原唱
  - 可以利用 AI/LLM 分析歌词内容来判断是否为原版歌词

- [ ] **语义化标题匹配**
  - 解决曲名表达差异问题（如"飞机场的十点半" vs "飞机场的10:30"）
  - 纯 fuzzy string matching 无法处理这种语义等价的情况
  - 需要 LLM 理解文字/数字表达差异，判断两个标题是否指向同一首歌

### 2. 获取专辑封面

- [ ] 使用 QQ Music 和网易云音乐获取专辑封面
  - 目前歌词源已实现，可以扩展获取 album artwork
  - QQ Music 和 NetEase 都提供专辑封面 URL

## Completed

- [x] 添加 QQ Music 歌词源
- [x] 添加网易云音乐歌词源
- [x] 修复 NetEase 搜索时加入 album 参数提高匹配准确性
- [x] 为 QQMusic 和 NetEase 添加调试日志
- [x] QQMusic 搜索时加入 album 参数（与 NetEase 保持一致）
- [x] 导入时繁体标签自动转换为简体（zhconv 插件）
- [x] 歌词繁体转简体（lyrics 插件 zh_style）
- [x] 解决歌词搜索标题繁简匹配问题