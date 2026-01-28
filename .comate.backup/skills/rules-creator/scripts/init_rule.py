#!/usr/bin/env python3
"""
规则初始化脚本

用法:
    python3 init_rule.py <rule-name>

示例:
    python3 init_rule.py my-new-rule
"""

import os
import sys
from pathlib import Path

RULE_TEMPLATE = '''---
description: [{rule_title}规则描述，一句话说明用途]
globs: [文件匹配模式，如 **/*.go, conf/**/*.toml]
alwaysApply: false
---

# Rule: {rule_title}

> [一句话说明规则用途]

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

```
```

### ❌ 错误示例

```
```

---

## 相关技能

- [skill-creator](../skills/skill-creator/SKILL.md) - 创建技能文档
'''


def create_rule(rule_name: str) -> None:
    """创建新规则文件"""
    
    # 确定规则目录路径
    script_dir = Path(__file__).parent.parent.parent.parent  # .comate/
    rules_dir = script_dir / "rules"
    rule_file = rules_dir / f"{rule_name}.mdr"
    
    if rule_file.exists():
        print(f"❌ 错误：规则文件已存在: {rule_file}")
        sys.exit(1)
    
    # 确保 rules 目录存在
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成规则标题（将连字符转换为空格并首字母大写）
    rule_title = rule_name.replace("-", " ").title()
    
    # 创建 .mdr 文件
    rule_content = RULE_TEMPLATE.format(
        rule_name=rule_name,
        rule_title=rule_title
    )
    rule_file.write_text(rule_content, encoding="utf-8")
    
    print(f"✅ 规则创建成功: {rule_file}")
    print(f"""
文件位置:
{rule_file}

下一步:
1. 编辑 {rule_file} 填充规则内容
2. 更新 YAML frontmatter 中的 description、globs、alwaysApply
3. 运行同步脚本更新索引:
   python3 .comate/skills/rules-creator/scripts/sync_rules.py
""")


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    
    rule_name = sys.argv[1].lower().strip()
    
    # 验证规则名称
    if not rule_name:
        print("❌ 错误：规则名称不能为空")
        sys.exit(1)
    
    if not all(c.isalnum() or c == "-" for c in rule_name):
        print("❌ 错误：规则名称只能包含字母、数字和连字符")
        sys.exit(1)
    
    create_rule(rule_name)


if __name__ == "__main__":
    main()