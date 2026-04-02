# AutoDev - 通用版小白全自动开发助手

> 一个面向**完全不懂代码**用户的自动化开发 SKILL。从需求分析 → 自动开发 → 测试 → 交付，全流程智能化。
>
> 支持 Vue / React / Angular / Python / Go / Java / Rust 等多种技术栈，**自动探测项目结构**后按需开发。

---

## 触发方式

在 Claude Code 中输入：

```
/autodev 我要在定价页添加一个年付/月付切换按钮，并且年付打8折
```

or

```
/autodev 我需要一个新的用户管理后台页面，能查看操作日志
```

---

## 工作流程（5阶段 SOP）

```
用户说需求
    ↓
阶段1：需求智能分析与验证
    → 提取功能点、评估合理性、必要时向用户澄清（最多3个问题）
    ↓
阶段2：任务拆解与 Agent 编排
    → 生成 architect / frontend / backend / tester / deliver 等专业 Agent
    → 使用 Ruflo workflow + swarm 进行编排
    → **backend-agent 按需召唤**
    ↓
阶段3：自动开发
    → 各 Agent 并行/顺序开发代码
    → **先读取 package.json / go.mod / pom.xml 推断技术栈**
    → 严格遵循项目现有规范
    ↓
阶段4：自动测试
    → 根据项目类型执行对应编译/构建命令
    → 功能验收测试
    → Bug 回退修复（最多3轮）
    ↓
阶段5：交付与归档
    → 生成大白话交付报告
    → Git 提交（征得同意后）
    → 更新项目文档进度
```

---

## 专业 Agent 说明

| Agent 类型 | 职责 | 配置文件 |
|-----------|------|---------|
| `architect-agent` | 技术方案设计、文件结构规划（**任何任务都必须先执行**） | `agents/architect.md` |
| `frontend-agent` | 前端页面/组件开发，自动适配 Vue/React/Angular/原生 | `agents/frontend.md` |
| `backend-agent` | 后端 API/数据库开发，**按需召唤**，自动适配 Go/Java/Python/Node.js/Rust | `agents/backend.md` |
| `tester-agent` | 编译检查 + 功能验收，自动调用 `npm build` / `mvn` / `go build` 等 | `agents/tester.md` |
| `deliver-agent` | 大白话交付报告 + 文档更新 | `agents/deliver.md` |

---

## 自动探测能力

AutoDev 启动时会**自动识别你的项目**：

| 探测项 | 依据文件 |
|--------|---------|
| Vue 前端 | `package.json` 中有 `vue` 依赖 |
| React 前端 | `package.json` 中有 `react` 依赖 |
| TypeScript | `package.json` 中有 `typescript` 依赖 |
| Go 后端 | 存在 `go.mod` |
| Java 后端 | 存在 `pom.xml` 或 `build.gradle` |
| Python 后端 | 存在 `requirements.txt` 或 `pyproject.toml` |
| Rust 后端 | 存在 `Cargo.toml` |

项目根目录默认从**当前工作目录**向上自动探测（查找 `package.json`、`pom.xml`、`go.mod` 等标志性文件）。

---

## 📦 安装方式

### 方式一：一键安装脚本（推荐）

```bash
cd autodev
bash install.sh
```

### 方式二：手动复制

将 `autodev` 文件夹放到：
```
Mac/Linux:   ~/.claude/skills/autodev/
Windows:     %USERPROFILE%\.claude\skills\autodev\
```

然后重启 Claude Code。

---

## ⚙️ 可选配置

如果你的项目结构很特殊，或者 AutoDev 探测不到根目录，可以配置环境变量：

```bash
# 强制指定项目根目录
export AUTODEV_PROJECT_ROOT="/Users/你的名字/你的项目"

# 强制指定记忆文件目录
export AUTODEV_MEMORY_DIR="/Users/你的名字/.claude/projects/.../memory"
```

建议加到 `~/.zshrc` 或 `~/.bashrc` 里。

---

## 示例需求

1. **UI 类**：`/autodev 定价页四个会员卡片太长了，希望可以在手机上左右滑动查看`
2. **功能类**：`/autodev 用户登录后，首页右上角显示当前会员等级的徽章图标`
3. **页面类**：`/autodev 新增一个「帮助中心」页面，列出常见问题和使用教程`
4. **逻辑类**：`/autodev 实验室发送 Prompt 时，如果不选模型要弹出提示而不是直接报错`
5. **后端类**：`/autodev 新增一个 API，用来记录用户的搜索历史`

---

## 注意事项

- 如果需求有歧义，Master Agent **会主动问你最多 3 个问题**，请尽量回答清楚。
- 如果涉及删除大量文件、修改数据库 schema、推送代码等危险操作，会**先征得你的同意**。
- 每完成一个阶段，会向你汇报进度，不会长时间静默运行。
- 如对任意技术栈有强烈的自定义偏好，可以在项目根目录下提供 `autodev.config.json` 配置文件覆盖自动推断结果。

---

## 📤 分享给其他小白用户

1. 将整个 `autodev` 文件夹压缩为 `autodev.zip` 发送给对方。
2. 对方解压后执行 `bash install.sh` 或手动复制到 `~/.claude/skills/autodev/`。
3. 重启 Claude Code 即可使用 `/autodev`。

> 💡 **这个 SKILL 是通用版！** 不绑定任何特定项目，会自动探测技术栈。你和朋友可以用在 Vue、React、Python、Go 等各种项目上。
