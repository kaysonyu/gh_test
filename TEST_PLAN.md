# 测试计划: PR 远程集群测试

## 1. 概述

本测试计划描述了在 GitHub PR 时自动触发远程集群测试的完整流程。

## 2. 关键 GitHub Context 变量

在 PR 工作流中，以下变量用于获取分支信息：

| 变量 | 描述 | 示例值 |
|------|------|--------|
| `github.head_ref` | PR 源分支名称 | `feature/new-feature` |
| `github.base_ref` | PR 目标分支名称 | `main` |
| `github.event.pull_request.number` | PR 编号 | `123` |
| `github.event.pull_request.head.sha` | PR 最新 commit SHA | `abc123def` |
| `github.event.pull_request.head.ref` | PR head 引用 | `feature/new-feature` |
| `github.repository` | 仓库名称 | `owner/repo` |

## 3. 测试阶段

### 3.1 阶段一: PR 信息提取

**目标**: 验证工作流能正确获取 PR 分支信息

**测试步骤**:
1. 创建一个新分支 `test/demo-branch`
2. 推送到远程并创建 PR
3. 查看 GitHub Actions 日志确认信息正确

**预期结果**:
- PR 编号正确显示
- 源分支名称正确 (`test/demo-branch`)
- 目标分支正确 (`main`)
- SHA 正确

### 3.2 阶段二: 本地测试

**目标**: 在 CI 环境中运行基础测试

**测试内容**:
- 单元测试 (`pytest tests/`)
- 代码检查 (可选)
- 构建验证

### 3.3 阶段三: 远程集群部署

**目标**: 验证能在远程集群切换到正确分支

**测试步骤**:
1. 连接到远程集群 (模拟)
2. 克隆/拉取代码
3. 切换到 PR 分支
4. 安装依赖
5. 启动应用

**验证点**:
- `BRANCH_INFO.txt` 包含正确的分支信息
- 应用能正常启动
- 环境变量正确传递

### 3.4 阶段四: 远程测试执行

**目标**: 在远程集群上运行完整测试套件

**测试类型**:
- 单元测试
- 集成测试
- 健康检查
- 性能测试 (可选)

## 4. 验证清单

### 4.1 PR 信息获取验证

- [ ] `github.head_ref` 返回正确的源分支
- [ ] `github.base_ref` 返回正确的目标分支
- [ ] `github.event.pull_request.number` 返回正确的 PR 编号
- [ ] `github.event.pull_request.head.sha` 返回正确的 commit SHA
- [ ] PR 信息能正确传递到后续 job

### 4.2 代码部署验证

- [ ] 代码能正确克隆到部署目录
- [ ] 分支切换成功
- [ ] 依赖安装成功
- [ ] 应用启动成功

### 4.3 测试执行验证

- [ ] 单元测试通过
- [ ] 健康检查通过
- [ ] 测试报告生成成功
- [ ] 测试结果反馈到 PR

## 5. 本地模拟测试

### 5.1 设置环境变量

```bash
export PR_NUMBER=123
export PR_BRANCH=feature/my-feature
export PR_BASE_BRANCH=main
export PR_SHA=abc123def456789
export PR_REPO=myorg/myrepo
```

### 5.2 运行部署脚本

```bash
chmod +x scripts/deploy-to-cluster.sh
bash scripts/deploy-to-cluster.sh
```

### 5.3 运行测试脚本

```bash
export DEPLOY_PATH=/tmp/cluster-deploy-123
chmod +x scripts/run-tests.sh
bash scripts/run-tests.sh
```

## 6. 自定义远程集群

要在实际的远程集群中运行，修改 `scripts/deploy-to-cluster.sh`:

```bash
# 配置你的集群
CLUSTER_HOST="your-cluster.example.com"
CLUSTER_USER="deploy"
CLUSTER_SSH_KEY="${CLUSTER_SSH_KEY:-~/.ssh/id_rsa}"

# SSH 连接并执行
ssh -i ${CLUSTER_SSH_KEY} ${CLUSTER_USER}@${CLUSTER_HOST} << EOF
  cd /opt/deployments
  git clone -b ${PR_BRANCH} https://github.com/${PR_REPO}.git pr-${PR_NUMBER}
  cd pr-${PR_NUMBER}
  # 安装依赖和运行测试
  pip install -r requirements.txt
  pytest tests/
EOF
```

## 7. 使用 Self-Hosted Runner

如果你的远程集群需要直接运行 GitHub Actions:

```yaml
jobs:
  test-on-cluster:
    runs-on: self-hosted  # 使用自托管 runner
    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - name: Run Tests
        run: |
          echo "Running on branch: ${{ github.head_ref }}"
          pytest tests/
```

## 8. 预期输出示例

### PR 信息输出
```
=== PR Information ===
PR Number: 42
PR Branch (head ref): feature/add-metrics
PR Base Branch: main
PR SHA: 7f3b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b
PR Repository: myorg/myrepo
```

### 部署成功输出
```
========================================
部署完成!
========================================
部署路径: /tmp/cluster-deploy-42
访问地址 (模拟): http://remote-cluster.example.com:8080/pr/42
========================================
```

### 测试报告输出
```
======================================
PR #42 测试报告
======================================
分支: feature/add-metrics
测试时间: 2024-01-15 10:30:00

测试结果:
  ✓ 单元测试: 通过
  ✓ 健康检查: 通过
  ✓ 集成测试: 通过
  ✓ 性能测试: 通过

总体状态: SUCCESS
======================================
```

## 9. 故障排除

### 问题: 无法获取 PR 分支名称
**解决**: 确保工作流在 `pull_request` 事件触发，使用 `github.head_ref` 而非 `github.ref`

### 问题: 远程集群连接失败
**解决**: 检查 SSH 密钥配置，确保 GitHub Secrets 中设置了正确的凭证

### 问题: 分支切换失败
**解决**: 确保远程仓库有足够权限，检查分支名称是否正确

## 10. 下一步

1. 将此项目推送到 GitHub
2. 创建一个测试分支
3. 提交 PR 并观察工作流执行
4. 根据实际集群环境修改部署脚本
