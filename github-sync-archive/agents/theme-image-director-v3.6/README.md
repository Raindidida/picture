# 主题驱动型母版生图 Agent｜导演探索版 v3.6

这是从 `C:/Users/1212/Desktop/tang_3.6_fixed_text.xlsx` 创建的 Agent 包。

## 文件

- `system_prompt.md`：完整系统提示词，可直接复制到 Agent / GPT / 工作流的 System Prompt。
- `agent.json`：Agent 元信息，包括名称、版本、入口文件和默认参数。

## 使用方式

1. 打开 `system_prompt.md`。
2. 将全文作为 Agent 的系统提示词。
3. 用户输入一个主题、关键词或短句，例如：`雨夜便利店`。
4. Agent 会按 v3.6 规则生成单张或系列图片提示词。

## 默认行为

- 模式：母版系列模式
- 数量：5
- 人数：单人
- 比例：9:16
- 当前环境无法生图时：输出完整提示词

## 来源

- 源文件：`C:\Users\1212\Desktop\tang_3.6_fixed_text.xlsx`
- 提取行数：787
