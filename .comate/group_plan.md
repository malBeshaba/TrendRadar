# TrendRadar 频率词组标题化改造计划

## 📋 项目背景
当前 `config/frequency_words.txt` 使用空行分隔的词组格式，在显示匹配新闻时会罗列词组内所有词，导致显示冗长不直观。

## 🎯 改造目标
1. 创建新的 YAML 格式配置文件 `config/frequency_groups.yaml`
2. 为每个词组添加可读的 title 标题
3. 在模板显示时使用 title 替代词组罗列
4. 保持对旧格式 `frequency_words.txt` 的向后兼容
5. 同步更新 MCP 服务的解析逻辑

## 📝 详细执行步骤

### ✅ 步骤 1：创建新的 YAML 配置文件
- **文件路径**: `config/frequency_groups.yaml`
- **操作类型**: 新增
- **任务内容**:
  - 根据现有 `frequency_words.txt` 内容创建 YAML 格式配置
  - 为每个词组添加合适的 title
  - 保持现有的 required/normal/filter 三种词类型
- **涉及文件**: `config/frequency_groups.yaml` (新建)
- **预期结果**: 完整的 YAML 格式配置文件，包含所有现有词组

### ✅ 步骤 2：修改主程序的频率词加载逻辑
- **文件路径**: `main.py`
- **操作类型**: 修改
- **涉及函数**: `load_frequency_words()` (约 LINE 672-750)
- **任务内容**:
  - 优先尝试加载 `frequency_groups.yaml`
  - 如果不存在则回退到 `frequency_words.txt`
  - 新增 YAML 格式解析逻辑
  - 返回的词组结构中添加 `title` 字段
- **预期结果**: 兼容新旧两种配置格式，新格式包含 title 信息

### ✅ 步骤 3：更新词组匹配逻辑
- **文件路径**: `main.py`
- **操作类型**: 修改
- **涉及函数**: `matches_word_groups()` (约 LINE 1009-1080)
- **任务内容**:
  - 确保匹配逻辑兼容新增的 title 字段
  - 保持现有的 required/normal/filter 匹配规则不变
- **预期结果**: 匹配逻辑正常工作，不受 title 字段影响

### ✅ 步骤 4：修改模板显示逻辑
- **文件路径**: `main.py`
- **操作类型**: 修改
- **涉及模块**: 生成报告相关的函数
- **搜索关键字**: `group_key`, 模板渲染相关代码
- **任务内容**:
  - 查找所有使用 `group_key` 显示词组的位置
  - 修改为优先使用 `title` 显示
  - 如果 title 不存在则回退到 group_key（兼容旧格式）
- **预期结果**: 报告中显示词组标题而非词组罗列

### ✅ 步骤 5：更新 MCP 服务的解析器
- **文件路径**: `mcp_server/services/parser_service.py`
- **操作类型**: 修改
- **涉及函数**: `parse_frequency_words()` (约 LINE 289-350)
- **任务内容**:
  - 添加对 `frequency_groups.yaml` 的解析支持
  - 保持对 `frequency_words.txt` 的兼容
  - 解析结果中包含 title 字段
- **预期结果**: MCP 服务能正确解析新旧两种格式

### ✅ 步骤 6：更新 MCP 数据服务
- **文件路径**: `mcp_server/services/data_service.py`
- **操作类型**: 修改
- **涉及位置**: 使用 `parse_frequency_words()` 的地方 (约 LINE 321, 431)
- **任务内容**:
  - 确保数据服务正确处理包含 title 的词组结构
  - 更新相关注释和文档字符串
- **预期结果**: MCP 数据服务正常工作

### ✅ 步骤 7：更新配置文件检查逻辑
- **文件路径**: `main.py`, `docker/manage.py`
- **操作类型**: 修改
- **涉及位置**: 
  - `main.py` 约 LINE 4670-4672
  - `docker/manage.py` 约 LINE 157-159
- **任务内容**:
  - 更新配置文件检查列表，添加 `frequency_groups.yaml`
  - 更新相关提示信息
- **预期结果**: 正确提示用户配置新的文件

### ✅ 步骤 8：更新项目文档
- **文件路径**: `README.md`
- **操作类型**: 修改
- **任务内容**:
  - 添加 `frequency_groups.yaml` 配置说明
  - 说明新旧格式的区别和迁移方法
  - 更新配置教程部分
- **预期结果**: 文档清晰说明新配置方式

### ✅ 步骤 9：测试验证
- **操作类型**: 验证
- **任务内容**:
  - 使用新配置文件运行主程序
  - 验证报告中显示的是 title 而非词组罗列
  - 验证 MCP 服务正常工作
  - 测试旧格式 `frequency_words.txt` 的兼容性
- **预期结果**: 所有功能正常，新旧格式都能工作

## 🔄 回滚方案
如果新功能出现问题：
1. 删除或重命名 `frequency_groups.yaml`
2. 程序会自动回退到使用 `frequency_words.txt`
3. 所有功能保持原有行为

## ⚠️ 注意事项
1. 保持代码的向后兼容性，不影响现有用户
2. YAML 解析需要 PyYAML 库（检查 requirements.txt 是否已包含）
3. 确保所有修改不破坏现有的匹配逻辑
4. title 字段为可选，如果不存在则使用原有的 group_key 显示

## 📦 依赖检查
- [ ] 检查 `requirements.txt` 是否包含 `PyYAML` 或 `pyyaml`