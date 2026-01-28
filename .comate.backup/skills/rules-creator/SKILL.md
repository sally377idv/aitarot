---
name: rules-creator
description: |
  创建和管理规则（元技能），支持新建规则、扫描校验、同步索引。
  **触发词**：新建rule、规则模板、.mdr结构、添加规则、创建规则、更新rules、同步rules、扫描rules、刷新规则索引、sync rules
  **使用场景**：新建规则文档、从社区复制规则后同步索引、校验规则格式
license: MIT
compatibility: claude-code, cursor, opencode, comate
metadata:
  audience: developers
  category: meta-skill
  project: your-project
---

# Skill: 规则创建指南

> 本技能指导如何为项目创建新的规则文档（.mdr 文件），遵循渐进式披露最佳实践。

## What I Do

- 提供规则创建的标准流程
- 提供 .mdr 模板和 YAML frontmatter 规范
- 说明规则的触发机制（globs、keywords、alwaysApply）
- 提供规则初始化和同步脚本

## When to Use Me

- 需要为项目添加新的规则文档
- 学习规则文档的结构和规范
- 从社区复制规则后，同步更新索引
- 扫描校验所有规则的格式规范

**不适用于**：
- 修改现有规则 → 直接编辑对应的 `.mdr` 文件
- 创建技能文档 → 参考 [skill-creator](../skill-creator/SKILL.md)

---

## 快速开始

### 方式一：使用初始化脚本（推荐）

```bash
python3 .comate/skills/rules-creator/scripts/init_rule.py <rule-name>
```

脚本会自动创建：
```
.comate/rules/<rule-name>.mdr   # 规则文件（模板已填充）
```

### 方式二：手动创建

1. 创建文件：`.comate/rules/<rule-name>.mdr`
2. 复制下方模板，填充内容
3. 运行同步脚本更新索引

---

## .mdr 规则模板

```markdown
---
description: [规则描述，一句话说明用途]
globs: [文件匹配模式，逗号分隔，如 **/*.go, conf/**/*.toml]
alwaysApply: false
---

# Rule: [规则名称]

> 一句话说明规则用途

## 触发条件

当修改以下路径时，必须遵守本规则：
- `path/pattern/**` - 说明

相关关键词：keyword1, keyword2, keyword3

---

## 核心约束

### 1. [约束名称]

[约束内容]

### 2. [约束名称]

[约束内容]

---

## 检查清单

- [ ] 检查项 1
- [ ] 检查项 2
- [ ] 检查项 3

---

## 示例

### ✅ 正确示例

[代码或说明]

### ❌ 错误示例

[代码或说明]

---

## 相关技能

- [skill-name](../skills/skill-name/SKILL.md) - 技能说明
```

---

## YAML Frontmatter 规范

规则文件必须以 YAML frontmatter 开头，包含以下字段：

| 字段 | 必填 | 说明 |
|-----|------|------|
| `description` | ✅ | 规则描述，一句话说明用途 |
| `globs` | 建议 | 文件匹配模式，逗号分隔 |
| `alwaysApply` | 建议 | 是否始终生效（true/false） |

### globs 字段说明

`globs` 用于指定规则适用的文件范围，支持 glob 模式：

| 模式 | 说明 | 示例 |
|-----|------|------|
| `**/*.go` | 所有 Go 文件 | 匹配 `src/services/handler.go` |
| `src/services/**` | 特定目录及子目录 | 匹配 `src/services/user/handler.go` |
| `conf/**/*.toml` | 特定类型配置 | 匹配 `conf/app.toml` |

多个模式用逗号分隔：`src/services/**,src/core/**`

### alwaysApply 字段说明

| 值 | 说明 | 适用场景 |
|---|------|---------|
| `true` | 对话启动时自动加载 | 工作流规则、全局规范 |
| `false` | 按需加载（globs 或关键词触发） | 特定领域规则 |

---

## 同步规则索引

当添加或删除规则后，使用同步脚本扫描并更新索引。

### 使用方式

```bash
# 扫描校验并更新 RULES_INDEX.md
python3 .comate/skills/rules-creator/scripts/sync_rules.py

# 仅扫描校验，不更新索引
python3 .comate/skills/rules-creator/scripts/sync_rules.py --dry-run
```

### 功能说明

1. **扫描**：遍历 `.comate/rules/` 下所有 `.mdr` 文件
2. **校验**：检查 YAML frontmatter 格式和必填字段
3. **报告**：输出校验结果（✅通过 / ⚠️警告 / ❌错误）
4. **同步**：自动更新 `RULES_INDEX.md`（新增/移除条目）

### 校验规则

| 检查项 | 级别 | 说明 |
|-------|------|------|
| .mdr 文件存在 | ERROR | 必须存在 |
| YAML frontmatter | ERROR | 必须以 `---` 开头和结尾 |
| description 字段 | ERROR | 必须有 description |
| globs 字段 | WARN | 建议指定文件匹配模式 |
| alwaysApply 字段 | WARN | 建议明确指定是否始终生效 |
| 包含触发条件 | WARN | 建议包含 `## 触发条件` 章节 |
| 包含检查清单 | WARN | 建议包含 `## 检查清单` 章节 |

---

## 创建后的检查清单

- [ ] `description` 字段清晰描述规则用途
- [ ] `globs` 字段正确匹配目标文件
- [ ] `alwaysApply` 字段根据场景正确设置
- [ ] 包含 `## 触发条件` 章节，说明适用场景
- [ ] 包含 `## 核心约束` 章节，说明具体规范
- [ ] 包含 `## 检查清单` 章节，便于自检
- [ ] 包含 `## 示例` 章节，提供正确/错误示例
- [ ] 已运行 `sync_rules.py` 更新 `RULES_INDEX.md`

---

## 规则 vs 技能

| 维度 | 规则 (.mdr) | 技能 (SKILL.md) |
|-----|------------|----------------|
| 触发方式 | 自动（globs/alwaysApply） | 显式/隐式调用 |
| 内容性质 | 强制约束、必须遵守 | 指导建议、可选参考 |
| 文件格式 | 单文件 `.mdr` | 目录结构 + `SKILL.md` |
| 典型用途 | 代码规范、工作流约束 | 开发指南、操作手册 |

---

## Related Rules

- [spec-mode.mdr](../../rules/spec-mode.mdr) - Spec Mode 工作流规则

## Related Skills

- [skill-creator](../skill-creator/SKILL.md) - 创建技能文档
- [specmode-init](../specmode-init/SKILL.md) - 初始化框架