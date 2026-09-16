# 包清单

`skills/` 包含 7 个技能、20 个文件。各技能均有 `SKILL.md` 和 `agents/openai.yaml`。

| 技能目录 | 额外资源 |
|---|---|
| `skills/reverse-research/` | `references/CANONICAL_CASES.md` |
| `skills/reverse-apk/` | 无 |
| `skills/reverse-native/` | 无 |
| `skills/reverse-protocol/` | 无 |
| `skills/reverse-state/` | `references/RETENTION_EXAMPLES.md`、`scripts/state.py` |
| `skills/reverse-toolbox/` | `references/ACQUISITION_POLICY.md`、`scripts/toolbox.py` |
| `skills/reverse-verify/` | `references/ORACLE_EXAMPLES.md` |

两个辅助脚本需要 Python 3.10+。

仓库根目录还包含中英文 README、升级说明和本清单。`assets/` 存放中英文架构图，由 `build_diagrams.py` 生成。
