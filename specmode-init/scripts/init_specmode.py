#!/usr/bin/env python3
"""
Spec Mode 框架初始化脚本

从 templates/ 目录复制完整的 .comate 框架到目标项目。
- .tmpl 文件会渲染变量后去掉后缀
- 其他文件直接复制

用法:
    python3 init_specmode.py [--name PROJECT_NAME] [--target TARGET_DIR]

参数:
    --name      项目名称，用于填充模板（默认从目录名推断）
    --target    目标目录（默认当前目录）

示例:
    python3 init_specmode.py
    python3 init_specmode.py --name "MyProject"
    python3 init_specmode.py --target /path/to/project
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def get_script_dir() -> Path:
    """获取脚本所在目录"""
    return Path(__file__).parent


def get_templates_dir() -> Path:
    """获取模板目录"""
    return get_script_dir().parent / "templates"


def render_template(content: str, variables: dict) -> str:
    """渲染模板，替换 {{variable}} 占位符"""
    result = content
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def copy_templates(templates_dir: Path, target_comate_dir: Path, variables: dict) -> dict:
    """
    递归复制模板目录到目标目录
    
    - .tmpl 文件：渲染变量后去掉 .tmpl 后缀
    - 其他文件：直接复制
    
    返回复制统计信息
    """
    stats = {
        "rendered": [],   # 渲染的模板文件
        "copied": [],     # 直接复制的文件
        "dirs": []        # 创建的目录
    }
    
    for item in templates_dir.rglob("*"):
        # 计算相对路径
        rel_path = item.relative_to(templates_dir)
        target_path = target_comate_dir / rel_path
        
        if item.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            stats["dirs"].append(str(rel_path))
        elif item.is_file():
            # 确保父目录存在
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            if item.suffix == ".tmpl":
                # 渲染模板文件
                try:
                    content = item.read_text(encoding="utf-8")
                    rendered_content = render_template(content, variables)
                    # 去掉 .tmpl 后缀
                    final_path = target_path.with_suffix("")
                    final_path.write_text(rendered_content, encoding="utf-8")
                    stats["rendered"].append(str(rel_path) + " → " + str(final_path.relative_to(target_comate_dir)))
                except Exception as e:
                    print(f"⚠️  渲染模板失败 {rel_path}: {e}")
            else:
                # 直接复制文件
                shutil.copy2(item, target_path)
                stats["copied"].append(str(rel_path))
    
    return stats


def init_specmode(target_dir: Path, project_name: str) -> bool:
    """初始化 Spec Mode 框架"""
    comate_dir = target_dir / ".comate"
    templates_dir = get_templates_dir()
    
    # 检查模板目录是否存在
    if not templates_dir.exists():
        print(f"❌ 错误：模板目录不存在: {templates_dir}")
        print("   请确保从完整的 specmode-init 技能目录运行此脚本")
        return False
    
    # 检查是否已存在 .comate 目录
    if comate_dir.exists():
        print(f"❌ 错误：目录已存在: {comate_dir}")
        print()
        print("请先备份并清空 .comate 目录后重试：")
        print(f"   1. 备份: cp -r {comate_dir} {comate_dir}.backup")
        print(f"   2. 清空: rm -rf {comate_dir}")
        print(f"   3. 重新执行此脚本")
        return False
    
    print(f"🚀 初始化 Spec Mode 框架...")
    print(f"   目标目录: {target_dir}")
    print(f"   项目名称: {project_name}")
    print()
    
    # 准备模板变量
    variables = {
        "project_name": project_name,
        "project_description": "（请填写项目描述）",
    }
    # 复制模板
    print("📁 创建目录结构并复制文件...")
    stats = copy_templates(templates_dir, comate_dir, variables)
    
    if stats["rendered"]:
        print(f"\n📄 渲染模板文件 ({len(stats['rendered'])} 个):")
        for f in stats["rendered"]:
            print(f"   ✅ {f}")
    
    if stats["copied"]:
        print(f"\n📋 复制文件 ({len(stats['copied'])} 个):")
        for f in stats["copied"][:10]:  # 最多显示10个
            print(f"   ✅ {f}")
        if len(stats["copied"]) > 10:
            print(f"   ... 及其他 {len(stats['copied']) - 10} 个文件")
    
    print()
    print("=" * 60)
    print("✅ Spec Mode 框架初始化完成!")
    print("=" * 60)
    print()
    print("生成的目录结构:")
    print(f"""
{comate_dir.relative_to(target_dir)}/
├── spec.md                     # 项目规范索引（请编辑）
├── rules/
│   ├── RULES_INDEX.md          # 规则索引
│   └── spec-mode.mdr           # Spec Mode 工作流规则
├── skills/
│   ├── SKILLS_INDEX.md         # 技能索引
│   ├── skill-creator/          # 元技能：创建技能
│   └── rules-creator/          # 元技能：创建规则
└── specs/
    ├── active/                 # 进行中的需求
    └── archive/                # 已归档需求
""")
    
    print("下一步:")
    print(f"  1. 编辑 {comate_dir / 'spec.md'} 填写项目信息")
    print(f"  2. 根据项目需要添加规则:")
    print(f"     python3 {comate_dir}/skills/rules-creator/scripts/init_rule.py <rule-name>")
    print(f"  3. 根据项目需要添加技能:")
    print(f"     python3 {comate_dir}/skills/skill-creator/scripts/init_skill.py <skill-name>")
    print()
    
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="初始化 Spec Mode 框架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--name", "-n",
        help="项目名称，用于填充模板（默认从目录名推断）"
    )
    parser.add_argument(
        "--target", "-t",
        default=".",
        help="目标目录（默认当前目录）"
    )
    
    args = parser.parse_args()
    
    # 解析目标目录
    target_dir = Path(args.target).resolve()
    if not target_dir.exists():
        print(f"❌ 目标目录不存在: {target_dir}")
        sys.exit(1)
    
    # 推断项目名称
    project_name = args.name
    if not project_name:
        project_name = target_dir.name
        # 将连字符和下划线转换为空格，首字母大写
        project_name = project_name.replace("-", " ").replace("_", " ").title()
    
    # 执行初始化
    success = init_specmode(target_dir, project_name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()