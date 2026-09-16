# 从旧版迁移

旧版采用 13 个编号技能和 3 个平台技能；当前版本改为 7 个按职责划分的技能。主要分工如下。

| 旧版职责 | 当前技能 |
|---|---|
| 安排分析步骤、调整方法、控制开销 | `reverse-research` |
| Android、原生、协议与文件格式分析 | `reverse-apk`、`reverse-native`、`reverse-protocol` |
| 进度记录、文件管理和交接 | `reverse-state` |
| 工具安装、登记、检查与清理 | `reverse-toolbox` |
| 定位结果、补丁和实际效果的检查 | `reverse-verify` |

## 安装迁移

1. 备份用户技能目录中属于本仓库旧版的 `00-reverse-research-orchestrator` 至 `12-reverse-knowledge-governance`，以及 `platform-android-apk`、`platform-native-binary`、`platform-protocol-fileformat` 三个目录。
2. 将这些旧版目录移出技能发现目录，避免同时匹配两套规则；不要批量删除其他来源的技能。
3. 将本仓库 `skills/` 下的 7 个目录复制到用户技能目录；同名目录先备份再替换。
4. 在后续任务中使用当前技能名称。

## 既有项目

已有项目可以继续使用。需要接着分析时，把当前目标、已查到的结果、卡住的问题和下一步写进 `.reverse/STATE.md`，附上相关文件的位置。

原件、重要证据和回退文件继续保留，不必为了升级重做分析或搬动全部历史文件。
