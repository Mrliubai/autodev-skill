#!/usr/bin/env bash
set -e

SKILL_NAME="autodev"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.claude/skills/${SKILL_NAME}"

echo "=========================================="
echo "🚀 AutoDev SKILL 安装脚本"
echo "=========================================="
echo ""

# 1. 检查目标目录
if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  检测到已存在旧版本，将覆盖..."
    rm -rf "$TARGET_DIR"
fi

# 2. 复制文件
echo "📦 正在安装到: $TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE_DIR/"* "$TARGET_DIR/"
chmod +x "$TARGET_DIR/run.py"

# 3. 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "❌ 未检测到 python3，请先安装 Python 3.8+"
    exit 1
fi

# 4. 安装简要提示
echo ""
echo "✅ 安装完成！"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📖 使用方式："
echo "   1. 确保你当前在 prompt-lab-vue 项目目录下"
echo "   2. 在 Claude Code 中输入："
echo ""
echo "      /autodev 我要在定价页添加年付/月付切换"
echo ""
echo "⚙️  可选配置（当你的项目路径特殊时）："
echo "   export AUTODEV_PROJECT_ROOT=/你的/项目/路径"
echo "   export AUTODEV_MEMORY_DIR=/你的/记忆/路径"
echo ""
echo "   可以把上面两行加到 ~/.zshrc 或 ~/.bashrc"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
