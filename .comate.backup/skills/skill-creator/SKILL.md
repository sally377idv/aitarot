---
name: skill-creator
description: |
  创建和管理技能（元技能），支持新建技能、扫描校验、同步索引。
  **触发词**：新建skill、技能模板、SKILL.md结构、添加技能、创建技能、更新skills、同步skills、扫描skills、刷新索引、sync skills
  **使用场景**：新建技能文档、从社区复制技能后同步索引
license: MIT
compatibility: claude-code, cursor, opencode, comate
metadata:
  audience: developers
  category: meta-skill
  project: your-project
---

# Skill: 技能创建指南

> 本技能指导如何为项目创建新的技能文档，遵循渐进式披露（Progressive Disclosure）最佳实践。

## What I Do

- 提供技能创建的标准流程
- 提供 SKILL.md 模板和 YAML frontmatter 规范
- 说明 references/ 和 scripts/ 目录的使用方法
- 提供技能初始化脚本

## When to Use Me

- 需要为项目添加新的技能文档
- 学习技能文档的结构和规范
- 创建可复用的知识能力包
- **从社区复制技能后，同步更新索引**
- **扫描校验所有技能的格式规范**

**不适用于**：
- 修改现有技能 → 直接编辑对应的 SKILL.md
- 创建规则文档 → 参考 `rules/*.mdr` 格式

---

## 快速开始

### 方式一：使用初始化脚本（推荐）

```bash
python3 .comate/skills/skill-creator/scripts/init_skill.py <skill-name>
```

脚本会自动创建：
```
.comate/skills/<skill-name>/
├── SKILL.md           # 主技能文件（模板已填充）
├── references/        # 详细参考文档目录
│   └── .gitkeep
└── scripts/           # 可执行脚本目录
    └── .gitkeep
```

### 方式二：手动创建

1. 创建目录：`.comate/skills/<skill-name>/`
2. 创建 `SKILL.md` 文件（使用下方模板）
3. 按需创建 `references/` 和 `scripts/` 目录

---

## SKILL.md 模板

```markdown
---
name: skill-name
description: |
  简明描述做什么（一句话）。
  **触发词**：关键词1、关键词2、关键词3
  **使用场景**：当用户需要做某事时使用
license: MIT
compatibility: claude-code, cursor, opencode, comate
metadata:
  audience: developers
  category: [category]
  project: your-project
---

# Skill: [技能名称]

> 一句话说明技能用途

## What I Do

- 核心能力 1
- 核心能力 2
- 核心能力 3

## When to Use Me

- 使用场景 1
- 使用场景 2

**不适用于**：
- 场景 1 → 参考 [其他技能](../other-skill/SKILL.md)

## Prerequisites

- 前置知识或依赖

---

## 核心概念

[精简的核心内容，控制在 ~100 行]

---

## 快速开始

[最常用的步骤，控制在 ~50 行]

---

## 深入学习

详细内容请参考：
- [详细说明 A](references/xxx.md)
- [完整示例](references/examples.md)

---

## Related Rules

- [rule-name.mdr](../../rules/rule-name.mdr) - 规则说明

## Related Skills

- [skill-name](../skill-name/SKILL.md) - 技能说明
```

---

## Description 编写规范

**Description 是技能自动触发的关键**，必须包含三个部分：

| 部分 | 说明 | 示例 |
|-----|------|------|
| **简述** | 一句话说明做什么 | 开发新服务模块，实现标准接口 |
| **触发词** | 用 `**触发词**：` 标记 | 新增服务、标准接口、服务注册 |
| **使用场景** | 用 `**使用场景**：` 标记 | 新增专业领域的服务模块 |

**好的 description 示例**：
```yaml
description: |
  开发新服务模块，实现标准接口。
  **触发词**：新增服务、标准接口、服务注册、模块开发
  **使用场景**：新增专业领域的服务模块
```

---

## 目录结构说明

### references/ 目录

存放详细参考文档，实现 LOD-2 按需加载：

| 文件类型 | 命名建议 | 用途 |
|---------|---------|------|
| 详细说明 | `xxx-detail.md` | 某个概念的深入解释 |
| 代码示例 | `examples.md` | 完整的代码示例 |
| 故障排除 | `troubleshooting.md` | 常见问题和解决方案 |

### scripts/ 目录

存放可执行脚本：

| 文件类型 | 命名建议 | 用途 |
|---------|---------|------|
| Shell 脚本 | `xxx.sh` | 自动化操作 |
| Python 脚本 | `xxx.py` | 复杂逻辑处理 |

**脚本优势**：执行脚本不占用上下文 Token。

---

## 创建后的检查清单

- [ ] `name` 字段使用小写字母和连字符
- [ ] `description` 包含简述 + 触发词 + 使用场景
- [ ] 主 SKILL.md 控制在 500 行以内
- [ ] 详细内容已拆分到 `references/` 目录
- [ ] 已更新 `SKILLS_INDEX.md` 添加新技能条目
- [ ] 已更新 `spec.md` 技能导航（如有必要）

---

## 同步技能索引

当从社区复制技能到 skills 目录后，使用同步脚本扫描并更新索引。

### 使用方式

```bash
# 扫描校验并更新 SKILLS_INDEX.md
python3 .comate/skills/skill-creator/scripts/sync_skills.py

# 仅扫描校验，不更新索引
python3 .comate/skills/skill-creator/scripts/sync_skills.py --dry-run
```

### 功能说明

1. **扫描**：遍历 `.comate/skills/` 下所有技能目录
2. **校验**：检查 SKILL.md 格式（YAML frontmatter、name、description、触发词、使用场景）
3. **报告**：输出校验结果（✅通过 / ⚠️警告 / ❌错误）
4. **同步**：自动更新 `SKILLS_INDEX.md`（新增/移除条目）

### 校验规则

| 检查项 | 级别 | 说明 |
|-------|------|------|
| SKILL.md 存在 | ERROR | 必须存在 |
| YAML frontmatter | ERROR | 必须以 `---` 开头和结尾 |
| name 字段 | ERROR | 必须有 name |
| description 字段 | ERROR | 必须有 description |
| 包含触发词 | WARN | 建议包含 `**触发词**：` |
| 包含使用场景 | WARN | 建议包含 `**使用场景**：` |

---

## Related Skills

- [rules-creator](../rules-creator/SKILL.md) - 创建规则文档
- [specmode-init](../specmode-init/SKILL.md) - 初始化框架