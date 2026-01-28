---
name: specmode-init
description: |
  初始化 Spec Mode 框架（元技能），一键创建 .comate/ 目录结构和核心文件。
  **触发词**：初始化specmode、init specmode、创建.comate目录、初始化spec mode框架、新项目接入、从零搭建、bootstrap specmode
  **使用场景**：新项目接入 Spec Mode 框架、从零搭建 AI 协作规范
license: MIT
compatibility: claude-code, cursor, opencode, comate
metadata:
  audience: developers
  category: meta-skill
  project: universal
---

# Skill: Spec Mode 框架初始化

> 一键创建 `.comate/` 目录结构和核心文件，帮助新项目快速接入 Spec Mode 框架。

## What I Do

- 从 `templates/` 目录复制完整的 `.comate/` 框架
- 自动渲染 `.tmpl` 模板文件，替换项目变量
- 包含所有元技能（skill-creator、rules-creator、specmode-init）
- 支持项目名称定制

## When to Use Me

- **新项目接入**：项目需要引入 Spec Mode 框架
- **从零搭建**：没有现成的 `.comate/` 目录需要创建
- **规范复制**：需要将 Spec Mode 框架应用到其他项目

**不适用于**：
- 已有 `.comate/` 目录只需更新 → 直接修改对应文件
- 只需创建技能 → 使用 [skill-creator](../skill-creator/SKILL.md)
- 只需创建规则 → 使用 [rules-creator](../rules-creator/SKILL.md)

---

## 快速开始

### 基础用法

```bash
# 在目标项目目录运行（从已有 specmode-init 技能复制）
python3 /path/to/specmode-init/scripts/init_specmode.py --target /path/to/new-project

# 指定项目名称
python3 /path/to/specmode-init/scripts/init_specmode.py --target /path/to/new-project --name "MyProject"

# 在当前目录初始化
python3 /path/to/specmode-init/scripts/init_specmode.py
```

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|-----|------|------|-------|
| `--name` | `-n` | 项目名称，用于填充模板 | 从目录名推断 |
| `--target` | `-t` | 目标目录 | 当前目录 |

---

## 模板目录结构

`templates/` 目录与目标 `.comate/` 目录结构完全一致：

```
templates/
├── spec.md.tmpl                    # → .comate/spec.md（渲染）
├── rules/
│   ├── RULES_INDEX.md.tmpl         # → 渲染
│   └── spec-mode.mdr               # → 直接复制
├── skills/
│   ├── SKILLS_INDEX.md.tmpl        # → 渲染
│   ├── skill-creator/              # → 直接复制
│   ├── rules-creator/              # → 直接复制
│   └── specmode-init/              # → 直接复制（自包含）
└── specs/
    ├── active/.gitkeep
    └── archive/.gitkeep
```

### 文件处理规则

| 文件类型 | 处理方式 |
|---------|---------|
| `*.tmpl` | 渲染变量后去掉 `.tmpl` 后缀 |
| 其他文件 | 直接复制 |

### 模板变量

| 变量 | 说明 | 示例 |
|-----|------|------|
| `{{project_name}}` | 项目名称 | My Project |
| `{{project_description}}` | 项目描述 | （请填写项目描述） |

---

## 生成的目录结构

```
{target}/.comate/
├── spec.md                     # 项目规范索引（需编辑）
│
├── rules/                      # 规则目录
│   ├── RULES_INDEX.md          # 规则索引（LOD-0）
│   └── spec-mode.mdr           # Spec Mode 工作流规则
│
├── skills/                     # 技能目录
│   ├── SKILLS_INDEX.md         # 技能索引（LOD-0）
│   ├── skill-creator/          # 元技能：创建技能
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── init_skill.py
│   │       └── sync_skills.py
│   ├── rules-creator/          # 元技能：创建规则
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── init_rule.py
│   │       └── sync_rules.py
│   └── specmode-init/          # 元技能：初始化框架（自包含）
│       ├── SKILL.md
│       ├── scripts/
│       │   └── init_specmode.py
│       └── templates/          # 完整模板（可用于初始化其他项目）
│
└── specs/                      # 变更管理目录
    ├── active/                 # 进行中的需求
    └── archive/                # 已归档需求
```

---

## 冲突处理

### 如果 .comate 目录已存在

脚本会报错并提示用户手动处理：

```
❌ 错误：目录已存在: /path/to/project/.comate

请先备份并清空 .comate 目录后重试：
   1. 备份: cp -r /path/to/project/.comate /path/to/project/.comate.backup
   2. 清空: rm -rf /path/to/project/.comate
   3. 重新执行此脚本
```

**设计原则**：不提供 `--force` 选项，避免意外覆盖用户的规则和技能定制。

---

## 初始化后的下一步

1. **编辑 spec.md**
   ```bash
   # 填写项目描述、核心原则、目录结构
   vim .comate/spec.md
   ```

2. **添加项目规则**
   ```bash
   # 创建项目特定的规则
   python3 .comate/skills/rules-creator/scripts/init_rule.py code-quality
   ```

3. **添加项目技能**
   ```bash
   # 创建项目特定的技能
   python3 .comate/skills/skill-creator/scripts/init_skill.py project-overview
   ```

4. **开始使用 Spec Mode**
   - 告诉 AI："开始 spec mode，我要实现 XXX 功能"
   - AI 会自动遵循 Spec Mode 工作流

---

## 自定义模板

如果需要为团队定制模板：

1. 复制整个 `specmode-init/templates/` 目录
2. 编辑模板文件，添加团队特定的规则和约定
3. 使用定制后的脚本初始化新项目

---

## FAQ

### Q: 如何只更新部分文件？

A: 不建议使用此脚本更新现有目录。请直接编辑对应文件，或使用相应的同步脚本：
- `sync_skills.py` - 更新技能索引
- `sync_rules.py` - 更新规则索引

### Q: 可以在已初始化的项目中运行吗？

A: 可以，但需要先备份并清空 `.comate` 目录。脚本不会自动覆盖。

### Q: 模板变量在哪些文件中生效？

A: 只有 `.tmpl` 后缀的文件会进行变量渲染。其他文件（如 Python 脚本、.mdr 规则）直接复制。

---

## Related Rules

- [spec-mode.mdr](../../rules/spec-mode.mdr) - Spec Mode 工作流规则

## Related Skills

- [skill-creator](../skill-creator/SKILL.md) - 创建技能文档
- [rules-creator](../rules-creator/SKILL.md) - 创建规则文档