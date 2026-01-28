#!/usr/bin/env python3
"""
技能同步脚本

扫描 .comate/skills/ 目录下所有技能，校验格式并更新 SKILLS_INDEX.md

用法:
    python3 sync_skills.py [--dry-run]

参数:
    --dry-run    仅扫描校验，不更新 SKILLS_INDEX.md
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


def validate_skill(skill_dir: Path) -> dict:
    """校验单个技能目录"""
    skill_md = skill_dir / "SKILL.md"
    result = {
        "name": skill_dir.name,
        "status": "pass",  # pass/warn/error
        "errors": [],
        "warnings": [],
        "description": "",
        "yaml_name": ""
    }
    
    # 检查 SKILL.md 存在
    if not skill_md.exists():
        result["status"] = "error"
        result["errors"].append("缺少 SKILL.md")
        return result
    
    # 读取并解析
    try:
        content = skill_md.read_text(encoding="utf-8")
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
    
    # 检查 name 字段
    if "name" not in frontmatter or not frontmatter["name"]:
        result["status"] = "error"
        result["errors"].append("缺少 name 字段")
    else:
        result["yaml_name"] = frontmatter["name"]
    
    # 检查 description 字段
    if "description" not in frontmatter or not frontmatter["description"]:
        result["status"] = "error"
        result["errors"].append("缺少 description 字段")
    else:
        desc = frontmatter["description"]
        result["description"] = desc
        
        # 检查触发词
        if "触发词" not in desc:
            result["warnings"].append("description 缺少触发词")
            if result["status"] == "pass":
                result["status"] = "warn"
        
        # 检查使用场景
        if "使用场景" not in desc:
            result["warnings"].append("description 缺少使用场景")
            if result["status"] == "pass":
                result["status"] = "warn"
    
    return result


def scan_skills(skills_dir: Path) -> list:
    """扫描所有技能目录"""
    results = []
    
    for item in sorted(skills_dir.iterdir()):
        # 跳过非目录、隐藏目录、特殊文件
        if not item.is_dir():
            continue
        if item.name.startswith('.'):
            continue
        
        result = validate_skill(item)
        results.append(result)
    
    return results


def generate_index_content(results: list) -> str:
    """生成 SKILLS_INDEX.md 内容"""
    lines = [
        "# 技能索引",
        "",
        "> 本索引在对话启动时加载，用于 AI Agent 判断何时激活相应技能。采用 LOD-0（Level of Detail）渐进式披露机制。",
        "",
        "## 技能列表",
        "",
        "| name | description |",
        "|------|-------------|",
    ]
    
    for r in results:
        if r["status"] == "error":
            continue  # 跳过有错误的技能
        
        name = r["yaml_name"] or r["name"]
        # 将 description 处理为单行，移除换行
        desc = r["description"].replace('\n', ' ').strip()
        # 转义表格中的管道符
        desc = desc.replace('|', '\\|')
        lines.append(f"| {name} | {desc} |")
    
    lines.extend([
        "",
        "## 加载机制",
        "",
        "```",
        "LOD-0（启动时）    LOD-1（触发时）       LOD-2（按需）",
        "┌─────────────┐   ┌─────────────────┐   ┌──────────────────┐",
        "│ 本索引文件   │ → │ 完整 SKILL.md   │ → │ references/      │",
        "│ ~50 行      │   │ <500 行        │   │ scripts/         │",
        "└─────────────┘   └─────────────────┘   └──────────────────┘",
        "```",
        "",
        "## 触发规则",
        "",
        "1. **显式调用**：用户明确提到技能名称或 `/skill-name` 命令",
        "2. **隐式调用**：用户请求中包含技能的**触发词**时自动匹配",
        "3. **文件关联**：编辑特定路径时参考 [规则加载](../spec.md#按需加载规则)",
        "",
        "## 相关文档",
        "",
        "- [spec.md](../spec.md) - 项目规范总索引",
        "- [rules/](../rules/) - 强制规则目录",
    ])
    
    return '\n'.join(lines)


def get_existing_skills(index_file: Path) -> set:
    """从现有 SKILLS_INDEX.md 获取技能列表"""
    if not index_file.exists():
        return set()
    
    content = index_file.read_text(encoding="utf-8")
    skills = set()
    
    # 匹配表格行
    for line in content.split('\n'):
        match = re.match(r'^\| (\S+) \|', line)
        if match and match.group(1) not in ('name', '------'):
            skills.add(match.group(1))
    
    return skills


def update_skills_index(skills_dir: Path, results: list, dry_run: bool = False) -> dict:
    """更新 SKILLS_INDEX.md"""
    index_file = skills_dir / "SKILLS_INDEX.md"
    
    # 获取现有技能
    existing = get_existing_skills(index_file)
    
    # 获取新技能（排除错误的）
    new_skills = {r["yaml_name"] or r["name"] for r in results if r["status"] != "error"}
    
    # 计算差异
    added = new_skills - existing
    removed = existing - new_skills
    
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
    print("\n🔍 扫描 .comate/skills/ 目录...\n")
    
    pass_count = 0
    warn_count = 0
    error_count = 0
    
    for r in results:
        name = r["name"]
        status = r["status"]
        
        if status == "pass":
            print(f"✅ {name} - 通过")
            pass_count += 1
        elif status == "warn":
            warnings = "; ".join(r["warnings"])
            print(f"⚠️  {name} - 警告: {warnings}")
            warn_count += 1
        else:
            errors = "; ".join(r["errors"])
            print(f"❌ {name} - 错误: {errors}")
            error_count += 1
    
    total = len(results)
    print(f"\n📊 扫描结果: {total} 个技能, {pass_count} 通过, {warn_count} 警告, {error_count} 错误")
    
    # 打印索引更新信息
    if diff["updated"]:
        print("\n🔄 更新 SKILLS_INDEX.md...")
        for name in diff["added"]:
            print(f"   + 新增: {name}")
        for name in diff["removed"]:
            print(f"   - 移除: {name}")
        if not diff["added"] and not diff["removed"]:
            print("   (无变化)")
        print("✅ SKILLS_INDEX.md 已更新")
    else:
        print("\n📝 --dry-run 模式，未更新 SKILLS_INDEX.md")
        if diff["added"]:
            print(f"   将新增: {', '.join(diff['added'])}")
        if diff["removed"]:
            print(f"   将移除: {', '.join(diff['removed'])}")


def main():
    """主函数"""
    dry_run = "--dry-run" in sys.argv
    
    # 确定技能目录路径
    script_path = Path(__file__).resolve()
    skills_dir = script_path.parent.parent.parent  # .comate/skills/
    
    if not skills_dir.exists():
        print(f"❌ 错误：技能目录不存在: {skills_dir}")
        sys.exit(1)
    
    # 扫描并校验
    results = scan_skills(skills_dir)
    
    if not results:
        print("⚠️  未找到任何技能目录")
        sys.exit(0)
    
    # 更新索引
    diff = update_skills_index(skills_dir, results, dry_run=dry_run)
    
    # 打印报告
    print_report(results, diff)


if __name__ == "__main__":
    main()