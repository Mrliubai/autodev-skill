#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoDev - 通用版小白全自动开发助手启动脚本
职责：自动探测项目根目录、技术栈、生成开发上下文
"""

import sys
import os
import json
import subprocess
from datetime import datetime

PROJECT_MARKERS = [
    "package.json",
    "pom.xml",
    "requirements.txt",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "frontend",
    "src",
]


def detect_project_root():
    """自动探测项目根目录"""
    env_root = os.environ.get("AUTODEV_PROJECT_ROOT", "").strip()
    if env_root and os.path.isdir(env_root):
        return os.path.abspath(env_root)

    cwd = os.getcwd()
    check_dir = cwd
    for _ in range(6):
        for marker in PROJECT_MARKERS:
            marker_path = os.path.join(check_dir, marker)
            if os.path.exists(marker_path):
                return os.path.abspath(check_dir)
        parent = os.path.dirname(check_dir)
        if parent == check_dir:
            break
        check_dir = parent
    return os.path.abspath(cwd)


def detect_memory_dir():
    """自动探测记忆目录"""
    env_mem = os.environ.get("AUTODEV_MEMORY_DIR", "").strip()
    if env_mem and os.path.isdir(env_mem):
        return os.path.abspath(env_mem)

    project_root = detect_project_root()
    clean_name = os.path.basename(project_root).replace(".", "-").replace("/", "-")
    default_project_dir = os.path.expanduser(f"~/.claude/projects/-Users-{get_username()}-{clean_name}/memory")
    if os.path.isdir(default_project_dir):
        return os.path.abspath(default_project_dir)

    # fallback: search in ~/.claude/projects
    projects_base = os.path.expanduser("~/.claude/projects")
    if os.path.isdir(projects_base):
        for d in os.listdir(projects_base):
            mem_path = os.path.join(projects_base, d, "memory")
            if os.path.isdir(mem_path):
                return os.path.abspath(mem_path)
    return os.path.abspath(default_project_dir)


def get_username():
    """获取当前用户名"""
    import getpass
    return getpass.getuser().replace(".", "-")


def infer_tech_stack(project_root):
    """根据项目文件推断技术栈"""
    stack = {
        "frontend": None,
        "backend": None,
        "build_tool": None,
        "language": None,
    }

    pkg_json = os.path.join(project_root, "package.json")
    if os.path.isfile(pkg_json):
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "vue" in deps:
                stack["frontend"] = "Vue"
            elif "react" in deps:
                stack["frontend"] = "React"
            elif "@angular/core" in deps:
                stack["frontend"] = "Angular"
            elif "svelte" in deps:
                stack["frontend"] = "Svelte"

            if "vite" in deps:
                stack["build_tool"] = "Vite"
            elif "webpack" in deps:
                stack["build_tool"] = "Webpack"

            if "typescript" in deps:
                stack["language"] = "TypeScript"
            else:
                stack["language"] = "JavaScript"
        except Exception:
            pass

    go_mod = os.path.join(project_root, "go.mod")
    if os.path.isfile(go_mod):
        stack["backend"] = "Go"
        if not stack["language"]:
            stack["language"] = "Go"

    pom = os.path.join(project_root, "pom.xml")
    if os.path.isfile(pom):
        stack["backend"] = "Java (Spring)"
        if not stack["language"]:
            stack["language"] = "Java"

    req_txt = os.path.join(project_root, "requirements.txt")
    pyproj = os.path.join(project_root, "pyproject.toml")
    if os.path.isfile(req_txt) or os.path.isfile(pyproj):
        stack["backend"] = "Python"
        if not stack["language"]:
            stack["language"] = "Python"

    cargo = os.path.join(project_root, "Cargo.toml")
    if os.path.isfile(cargo):
        stack["backend"] = "Rust"
        if not stack["language"]:
            stack["language"] = "Rust"

    # 目录推断
    if os.path.isdir(os.path.join(project_root, "frontend")) and not stack["frontend"]:
        stack["frontend"] = "Unknown (frontend/ detected)"
    if os.path.isdir(os.path.join(project_root, "backend")) and not stack["backend"]:
        stack["backend"] = "Unknown (backend/ detected)"

    return stack


def check_environment(project_root):
    """检查项目环境状态"""
    frontend_dir = os.path.join(project_root, "frontend")
    backend_dir = os.path.join(project_root, "backend")
    # 如果没有 frontend 目录但根目录有 package.json，根目录就是前端
    if not os.path.isdir(frontend_dir) and os.path.isfile(os.path.join(project_root, "package.json")):
        frontend_dir = project_root

    return {
        "project_exists": os.path.isdir(project_root),
        "frontend_exists": os.path.isdir(frontend_dir) or os.path.isfile(os.path.join(frontend_dir, "package.json")),
        "backend_exists": os.path.isdir(backend_dir),
        "git_repo": os.path.isdir(os.path.join(project_root, ".git")),
        "node_modules_exists": os.path.isdir(os.path.join(frontend_dir, "node_modules")),
    }


def get_git_status(project_root):
    """获取当前 git 状态摘要"""
    if not os.path.isdir(os.path.join(project_root, ".git")):
        return {"branch": "N/A", "clean": True, "changes": 0}
    try:
        branch = subprocess.check_output(
            ["git", "-C", project_root, "rev-parse", "--abbrev-ref", "HEAD"],
            text=True
        ).strip()
        changes = subprocess.check_output(
            ["git", "-C", project_root, "status", "--short"],
            text=True
        ).strip()
        return {
            "branch": branch,
            "clean": len(changes) == 0,
            "changes": len([l for l in changes.split("\n") if l.strip()]) if changes else 0
        }
    except Exception:
        return {"branch": "unknown", "clean": True, "changes": 0}


def get_memory_context(memory_dir):
    """读取关键记忆文件是否存在"""
    files = {
        "MEMORY": os.path.join(memory_dir, "MEMORY.md"),
        "PRD": os.path.join(memory_dir, "PRD.md"),
        "code_decisions": os.path.join(memory_dir, "code-decisions.md"),
        "project_todos": os.path.join(memory_dir, "project-todos.md"),
    }
    return {k: os.path.exists(v) for k, v in files.items()}


def print_banner():
    print("=" * 60)
    print("🚀 AutoDev 通用版小白全自动开发助手已启动")
    print("=" * 60)


def main():
    raw_requirement = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""

    print_banner()

    if not raw_requirement:
        print("\n⚠️  未检测到需求描述。")
        print("用法示例：/autodev 我要在定价页添加一个年付/月付切换按钮")
        print("\n如需设置项目路径，可添加环境变量：")
        print("   export AUTODEV_PROJECT_ROOT=/你的/项目/路径")
        print("   export AUTODEV_MEMORY_DIR=/你的/记忆/路径")
        sys.exit(0)

    project_root = detect_project_root()
    memory_dir = detect_memory_dir()
    tech_stack = infer_tech_stack(project_root)
    env_status = check_environment(project_root)
    git_status = get_git_status(project_root)
    memory_status = get_memory_context(memory_dir)

    print(f"\n📄 原始需求：{raw_requirement}\n")
    print(f"🔧 探测到项目根目录：{project_root}")
    print(f"🔧 探测到记忆目录：{memory_dir}")
    print(f"🔧 推断技术栈：{json.dumps(tech_stack, ensure_ascii=False)}\n")

    print("🔍 环境预检结果：")
    print(f"   项目根目录: {'✅' if env_status['project_exists'] else '❌'}")
    print(f"   前端目录:   {'✅' if env_status['frontend_exists'] else '❌'}")
    print(f"   后端目录:   {'✅' if env_status['backend_exists'] else '❌'}")
    print(f"   Git 仓库:   {'✅' if env_status['git_repo'] else '❌'} (分支: {git_status['branch']})")
    print(f"   未提交变更: {git_status['changes']} 处")
    print(f"   node_modules: {'✅' if env_status['node_modules_exists'] else '❌'}")
    print(f"   记忆文件:   MEMORY{'✅' if memory_status['MEMORY'] else '❌'} | PRD{'✅' if memory_status['PRD'] else '❌'} | 规范{'✅' if memory_status['code_decisions'] else '❌'}")

    context = {
        "timestamp": datetime.now().isoformat(),
        "raw_requirement": raw_requirement,
        "project_root": project_root,
        "memory_dir": memory_dir,
        "tech_stack": tech_stack,
        "environment": env_status,
        "git_status": git_status,
        "memory_files": memory_status,
        "stage": "INIT_COMPLETE",
        "next_action": "MASTER_AGENT 应继续执行：需求分析 → 任务拆解 → 开发 → 测试 → 交付"
    }

    print("\n" + "=" * 60)
    print("🧠 启动上下文（供 Master Agent 读取）：")
    print("=" * 60)
    print(json.dumps(context, ensure_ascii=False, indent=2))
    print("\n✅ 预检完成。Master Agent 请接管后续流程。")


if __name__ == "__main__":
    main()
