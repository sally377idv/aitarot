# Spec Mode 框架初始化工具

一键为新项目创建 `.comate/` 目录结构和核心文件，快速接入 Spec Mode 框架。

## 环境要求

- **Python 3.6+**（无需安装额外依赖，仅使用标准库）

## 快速开始

### 1. 下载并解压

将 `specmode-init.zip` 解压到项目根目录：

```bash
# 方式1：解压到项目根目录
unzip specmode-init.zip -d /path/to/your-project/

# 方式2：复制目录（如果已有源文件）
cp -r specmode-init /path/to/your-project/
```

### 2. 运行初始化

```bash
cd /path/to/your-project
python3 ./specmode-init/scripts/init_specmode.py --target ./
```

或指定项目名称：

```bash
python3 ./specmode-init/scripts/init_specmode.py --target ./ --name "My Project"
```

### 3. 清理（可选）

初始化完成后，可以删除 `specmode-init` 目录：

```bash
rm -rf ./specmode-init
```

## 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|-----|------|------|-------|
| `--name` | `-n` | 项目名称，用于填充模板 | 从目录名推断 |
| `--target` | `-t` | 目标目录 | 当前目录 |

## 初始化后的目录结构

```
your-project/
├── .comate/
│   ├── spec.md                 # 项目规范索引（请编辑）
│   ├── rules/
│   │   ├── RULES_INDEX.md      # 规则索引
│   │   └── spec-mode.mdr       # Spec Mode 工作流规则
│   ├── skills/
│   │   ├── SKILLS_INDEX.md     # 技能索引
│   │   ├── skill-creator/      # 元技能：创建技能
│   │   └── rules-creator/      # 元技能：创建规则
│   └── specs/
│       ├── active/             # 进行中的需求
│       └── archive/            # 已归档需求
└── specmode-init/              # 可删除
```

## 初始化后的下一步

1. **编辑 spec.md** - 填写项目描述、核心原则、目录结构
   ```bash
   vim .comate/spec.md
   ```

2. **添加项目规则**
   ```bash
   python3 .comate/skills/rules-creator/scripts/init_rule.py code-quality
   ```

3. **添加项目技能**
   ```bash
   python3 .comate/skills/skill-creator/scripts/init_skill.py project-overview
   ```

4. **开始使用 Spec Mode**
   - 告诉 AI："开始 spec mode，我要实现 XXX 功能"
   - AI 会自动遵循三文档流程：`doc.md` → `tasks.md` → `summary.md`

## 冲突处理

如果目标项目已有 `.comate` 目录，脚本会提示错误并建议：
1. 备份现有目录
2. 手动清空后重试

不支持自动覆盖，以防止意外丢失用户的规则和技能定制。

## 文件说明

```
specmode-init/
├── README.md               # 本文档
├── SKILL.md                # 技能说明文档
├── scripts/
│   └── init_specmode.py    # 初始化脚本（Python 3.6+ 标准库）
└── templates/              # 模板目录
    ├── spec.md.tmpl        # 项目规范模板
    ├── rules/              # 规则模板
    ├── skills/             # 技能模板
    └── specs/              # 需求目录模板
```

## 许可证

MIT