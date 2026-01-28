#!/usr/bin/env python3
"""
技能初始化脚本

用法:
    python3 init_skill.py <skill-name>

示例:
    python3 init_skill.py my-new-skill
"""

import os
import sys
from pathlib import Path

SKILL_TEMPLATE = '''---
name: {skill_name}
description: |
  [简明描述做什么，一句话]。
  **触发词**：关键词1、关键词2、关键词3
  **使用场景**：当用户需要做某事时使用
license: MIT
compatibility: claude-code, cursor, opencode, comate
metadata:
  audience: developers
  category: [category]
  project: your-project
---

# Skill: {skill_title}

> [一句话说明技能用途]

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
- [详细说明](references/detail.md)

---

## Related Rules

- [spec-mode.mdr](../../rules/spec-mode.mdr) - Spec Mode 工作流规则

## Related Skills

- [skill-creator](../skill-creator/SKILL.md) - 创建技能文档
'''


def create_skill(skill_name: str) -> None:
    """创建新技能的目录结构并初始化相关文件"""
    
    # 确定技能目录路径
    script_dir = Path(__file__).parent.parent.parent  # .comate/skills/
    skill_dir = script_dir / skill_name
    
    if skill_dir.exists():
        print(f"❌ 错误：技能目录已存在: {skill_dir}")
        sys.exit(1)
    
    # 创建目录结构
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "scripts").mkdir(parents=True)
    
    # 创建 .gitkeep 文件
    (skill_dir / "references" / ".gitkeep").touch()
    (skill_dir / "scripts" / ".gitkeep").touch()
    
    # 生成技能标题（将连字符转换为空格并首字母大写）
    skill_title = skill_name.replace("-", " ").title()
    
    # 创建 SKILL.md
    skill_md_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )
    (skill_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")
    
    print(f"✅ 技能创建成功: {skill_dir}")
    print(f"""
目录结构:
{skill_dir}/
├── SKILL.md           # 主技能文件（请编辑）
├── references/        # 详细参考文档目录
│   └── .gitkeep
└── scripts/           # 可执行脚本目录
    └── .gitkeep

下一步:
1. 编辑 {skill_dir}/SKILL.md 填充技能内容
2. 在 references/ 中添加详细文档
3. 运行同步脚本更新索引:
   python3 .comate/skills/skill-creator/scripts/sync_skills.py
""")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    
    skill_name = sys.argv[1].lower().strip()
    
    # 验证技能名称
    if not skill_name:
        print("❌ 错误：技能名称不能为空")
        sys.exit(1)
    
    if not all(c.isalnum() or c == "-" for c in skill_name):
        print("❌ 错误：技能名称只能包含字母、数字和连字符")
        sys.exit(1)
    
    create_skill(skill_name)


if __name__ == "__main__":
    main()