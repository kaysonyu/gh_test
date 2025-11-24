# GitHub PR 远程集群测试 Demo

这个项目演示了如何在 GitHub PR 时自动在远程集群切换到对应分支进行测试。

## 项目结构

```
.
├── .github/
│   └── workflows/
│       └── pr-test.yml          # PR 触发的工作流
├── app/
│   ├── main.py                  # 示例应用程序
│   └── requirements.txt         # Python 依赖
├── scripts/
│   ├── deploy-to-cluster.sh     # 部署到远程集群的脚本
│   └── run-tests.sh             # 测试脚本
├── tests/
│   └── test_app.py              # 单元测试
└── README.md
```

## 核心功能

### 1. GitHub 工作流获取 PR 分支信息

工作流会自动获取以下信息：
- PR 源分支名称
- PR 目标分支名称
- PR 编号
- 提交 SHA
- 仓库信息

### 2. 远程集群部署

模拟在远程集群中：
- 克隆/拉取代码
- 切换到 PR 分支
- 运行测试
- 报告结果

## 快速开始

### 本地测试

```bash
# 安装依赖
pip install -r app/requirements.txt

# 运行应用
python app/main.py

# 运行测试
python -m pytest tests/
```

### 模拟 PR 工作流

```bash
# 设置环境变量模拟 PR 环境
export PR_NUMBER=123
export PR_BRANCH=feature/new-feature
export PR_BASE_BRANCH=main
export PR_SHA=abc123def456

# 运行部署脚本
bash scripts/deploy-to-cluster.sh
```

## 测试计划

详细的测试计划请查看 `TEST_PLAN.md`

## 工作流说明

当创建或更新 PR 时：
1. GitHub Actions 自动触发
2. 工作流获取 PR 分支信息
3. 连接到远程集群（本 demo 中模拟）
4. 在集群中切换到 PR 分支
5. 运行自动化测试
6. 将测试结果报告回 PR
