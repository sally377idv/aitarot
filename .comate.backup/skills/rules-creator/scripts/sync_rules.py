#!/usr/bin/env python3
"""
规则同步脚本

扫描 .comate/rules/ 目录下所有 .mdr 文件，校验格式并更新 RULES_INDEX.md

用法:
    python3 sync_rules.py [--dry-run]

参数:
    --dry-run    仅扫描校验，不更新 RULES_INDEX.md
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional


def parse_frontmatter(content: str) -> Optional[dict]:
    """解析 YAML frontmatter"""
    if not content.startswith("---"):
        return None
    
    # 查找第二个 ---
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return None
    
    yaml_content = content[3:end_match.start() + 3]
    
    # 简单解析 YAML（不依赖 pyyaml）
    result = {}
    current_key = None
    current_value = []
    
    for line in yaml_content.split('\n'):
        # 检查是否是新的顶级键
        key_match = re.match(r'^(\w+):\s*(.*)', line)
        if key_match:
            # 保存之前的键值
            if current_key:
                value = '\n'.join(current_value).strip()
                if value.startswith('|'):
                    value = '\n'.join(current_value[1:]) if len(current_value) > 1 else ''
                result[current_key] = value.strip()
            
            current_key = key_match.group(1)
            current_value = [key_match.group(2)] if key_match.group(2) else []
        elif current_key and (line.startswith('  ') or line.strip() == ''):
            current_value.append(line)
    
    # 保存最后一个键值
    if current_key:
        value = '\n'.join(current_value).strip()
        if value.startswith('|'):
            value = '\n'.join(current_value[1:]) if len(current_value) > 1 else ''
        result[current_key] = value.strip()
    
    return result if result else None


def extract_keywords(content: str) -> list:
    """从规则内容中提取关键词"""
    keywords = []
    
    # 从 "相关关键词" 或 "关键词" 行提取
    keyword_match = re.search(r'相关关键词[：:]\s*(.+)', content)
    if keyword_match:
        keywords_str = keyword_match.group(1)
        keywords = [k.strip() for k in re.split(r'[,，、]', keywords_str) if k.strip()]
    
    return keywords


def validate_rule(rule_file: Path) -> dict:
    """校验单个规则文件"""
    result = {
        "name": rule_file.stem,  # 文件名（不含扩展名）
        "status": "pass",  # pass/warn/error
        "errors": [],
        "warnings": [],
        "description": "",
        "globs": "",
        "alwaysApply": False,
        "keywords": []
    }
    
    # 读取文件
    try:
        content = rule_file.read_text(encoding="utf-8")
    except Exception as e:
        result["status"] = "error"
        result["errors"].append(f"读取文件失败: {e}")
        return result
    
    # 解析 YAML frontmatter
    frontmatter = parse_frontmatter(content)
    
    if not frontmatter:
        result["status"] = "error"
        result["errors"].append("缺少或无法解析 YAML frontmatter")
        return result
    
    # 检查 description 字段
    if "description" not in frontmatter or not frontmatter["description"]:
        result["status"] = "error"
        result["errors"].append("缺少 description 字段")
    else:
        result["description"] = frontmatter["description"]
    
    # 检查 globs 字段
    if "globs" not in frontmatter:
        result["warnings"].append("缺少 globs 字段")
        if result["status"] == "pass":
            result["status"] = "warn"
    else:
        result["globs"] = frontmatter.get("globs", "")
    
    # 检查 alwaysApply 字段
    if "alwaysApply" not in frontmatter:
        result["warnings"].append("缺少 alwaysApply 字段")
        if result["status"] == "pass":
            result["status"] = "warn"
    else:
        always_apply = frontmatter.get("alwaysApply", "").lower()
        result["alwaysApply"] = always_apply == "true"
    
    # 检查触发条件章节
    if "## 触发条件" not in content:
        result["warnings"].append("缺少 ## 触发条件 章节")
        if result["status"] == "pass":
            result["status"] = "warn"
    
    # 检查检查清单章节
    if "## 检查清单" not in content:
        result["warnings"].append("缺少 ## 检查清单 章节")
        if result["status"] == "pass":
            result["status"] = "warn"
    
    # 提取关键词
    result["keywords"] = extract_keywords(content)
    
    return result


def scan_rules(rules_dir: Path) -> list:
    """扫描所有规则文件"""
    results = []
    
    for item in sorted(rules_dir.iterdir()):
        # 只处理 .mdr 文件
        if not item.is_file():
            continue
        if not item.suffix == ".mdr":
            continue
        if item.name.startswith('.'):
            continue
        
        result = validate_rule(item)
        results.append(result)
    
    return results


def generate_index_content(results: list) -> str:
    """生成 RULES_INDEX.md 内容"""
    lines = [
        "# 规则索引",
        "",
        "> 本索引在对话启动时加载，用于 AI Agent 判断何时激活相应规则。采用 LOD-0（Level of Detail）渐进式披露机制。",
        "",
        "## 规则列表",
        "",
        "| name | description | globs | alwaysApply | keywords |",
        "|------|-------------|-------|-------------|----------|",
    ]
    
    for r in results:
        if r["status"] == "error":
            continue  # 跳过有错误的规则
        
        name = r["name"]
        # 将 description 处理为单行
        desc = r["description"].replace('\n', ' ').strip()
        # 转义表格中的管道符
        desc = desc.replace('|', '\\|')
        
        # globs 处理
        globs = r["globs"]
        if globs:
            # 格式化 globs，添加代码标记
            globs_list = [g.strip() for g in globs.split(',') if g.strip()]
            globs = ', '.join(f'`{g}`' for g in globs_list)
        else:
            globs = "-"
        
        # alwaysApply 处理
        always_apply = "✅" if r["alwaysApply"] else "❌"
        
        # keywords 处理
        keywords = ", ".join(r["keywords"]) if r["keywords"] else "-"
        
        lines.append(f"| {name} | {desc} | {globs} | {always_apply} | {keywords} |")
    
    lines.extend([
        "",
        "## 加载机制",
        "",
        "```",
        "LOD-0（启动时）    LOD-1（触发时）",
        "┌─────────────┐   ┌─────────────────┐",
        "│ 本索引文件   │ → │ 完整 .mdr 文件  │",
        "│ ~30 行      │   │ <300 行        │",
        "└─────────────┘   └─────────────────┘",
        "```",
        "",
        "## 触发规则",
        "",
        "1. **始终生效**（alwaysApply: ✅）：对话启动时自动加载完整规则",
        "2. **文件匹配**（globs）：编辑匹配路径时加载对应规则",
        "3. **关键词匹配**（keywords）：用户请求中包含关键词时自动匹配",
        "",
        "### 触发示例",
        "",
        "| 用户行为 | 触发的规则 |",
        "|---------|-----------|",
        '| 说"开始 spec mode" | `spec-mode`（始终生效） |',
        "| 编辑 `src/services/user.go` | 匹配 globs 的规则 |",
        '| 说"新增一个功能" | 匹配关键词的规则 |',
        "",
        "## 相关文档",
        "",
        "- [spec.md](../spec.md) - 项目规范总索引",
        "- [skills/](../skills/) - 技能目录",
    ])
    
    return '\n'.join(lines)


def get_existing_rules(index_file: Path) -> set:
    """从现有 RULES_INDEX.md 获取规则列表"""
    if not index_file.exists():
        return set()
    
    content = index_file.read_text(encoding="utf-8")
    rules = set()
    
    # 匹配表格行
    for line in content.split('\n'):
        match = re.match(r'^\| (\S+) \|', line)
        if match and match.group(1) not in ('name', '------'):
            rules.add(match.group(1))
    
    return rules


def update_rules_index(rules_dir: Path, results: list, dry_run: bool = False) -> dict:
    """更新 RULES_INDEX.md"""
    index_file = rules_dir / "RULES_INDEX.md"
    
    # 获取现有规则
    existing = get_existing_rules(index_file)
    
    # 获取新规则（排除错误的）
    new_rules = {r["name"] for r in results if r["status"] != "error"}
    
    # 计算差异
    added = new_rules - existing
    removed = existing - new_rules
    
    diff = {
        "added": sorted(added),
        "removed": sorted(removed),
        "updated": not dry_run
    }
    
    if not dry_run:
        new_content = generate_index_content(results)
        index_file.write_text(new_content, encoding="utf-8")
    
    return diff


def print_report(results: list, diff: dict):
    """打印校验报告"""
    print("\n🔍 扫描 .comate/rules/ 目录...\n")
    
    pass_count = 0
    warn_count = 0
    error_count = 0
    
    for r in results:
        name = r["name"]
        status = r["status"]
        
        if status == "pass":
            print(f"✅ {name}.mdr - 通过")
            pass_count += 1
        elif status == "warn":
            warnings = "; ".join(r["warnings"])
            print(f"⚠️  {name}.mdr - 警告: {warnings}")
            warn_count += 1
        else:
            errors = "; ".join(r["errors"])
            print(f"❌ {name}.mdr - 错误: {errors}")
            error_count += 1
    
    total = len(results)
    print(f"\n📊 扫描结果: {total} 个规则, {pass_count} 通过, {warn_count} 警告, {error_count} 错误")
    
    # 打印索引更新信息
    if diff["updated"]:
        print("\n🔄 更新 RULES_INDEX.md...")
        for name in diff["added"]:
            print(f"   + 新增: {name}")
        for name in diff["removed"]:
            print(f"   - 移除: {name}")
        if not diff["added"] and not diff["removed"]:
            print("   (无变化)")
        print("✅ RULES_INDEX.md 已更新")
    else:
        print("\n📝 --dry-run 模式，未更新 RULES_INDEX.md")
        if diff["added"]:
            print(f"   将新增: {', '.join(diff['added'])}")
        if diff["removed"]:
            print(f"   将移除: {', '.join(diff['removed'])}")


def main():
    """主函数"""
    dry_run = "--dry-run" in sys.argv
    
    # 确定规则目录路径
    script_path = Path(__file__).resolve()
    rules_dir = script_path.parent.parent.parent / "rules"  # .comate/rules/
    
    if not rules_dir.exists():
        print(f"❌ 错误：规则目录不存在: {rules_dir}")
        sys.exit(1)
    
    # 扫描并校验
    results = scan_rules(rules_dir)
    
    if not results:
        print("⚠️  未找到任何 .mdr 规则文件")
        sys.exit(0)
    
    # 更新索引
    diff = update_rules_index(rules_dir, results, dry_run=dry_run)
    
    # 打印报告
    print_report(results, diff)


if __name__ == "__main__":
    main()