# Jane Street Fork Snapshot · Agent Skills / Socratic Tutor

这是 P-Research 对 **Jane Street `agent_skills` / `socratic-tutor` 的目录内源码副本**。
引入日期：2026-11-13。上游六个文件保持原样，中文解释与验证工具在外层。

这里的 fork 指可追溯的 vendored snapshot，**不是新建 GitHub fork 仓库或平台 parent 关系**。
不代表 Jane Street 与 P-Research 合作、推荐、认可或提供招聘机会。

## 1. Jane Street Origin

- 发布组织：[janestreet/agent_skills](https://github.com/janestreet/agent_skills)。
- 官方源提交：[7c6715c29548a3b39d4a9545c698ee4fd17a7213](https://github.com/janestreet/agent_skills/commit/7c6715c29548a3b39d4a9545c698ee4fd17a7213)。
- 默认分支：`master`；该提交时间为 2026-11-03，Git 作者为 `public-release`。
  这不足以认定某个具体自然人是作者，因此不推测个人作者。
- 许可证：MIT；版权属于 `Jane Street Group, LLC`，保留原始
  [LICENSE.md](upstream/LICENSE.md) 和 [CONTRIBUTING.md](upstream/CONTRIBUTING.md)。
- 根 Git Tree：`6dd590cb153ac1e0073914cb2e89029d9fdef04e`。
- 原始技能：[upstream/socratic-tutor/SKILL.md](upstream/socratic-tutor/SKILL.md)。

上游公开的是一个给 LLM 使用的教学协议，不是独立模型、训练权重、Agent 调度器、
交易系统或 Jane Street 内部面试题库。它也不是对苏格拉底教学法本身的原创权声明。
没有证据证明它用于 Jane Street 的内部招聘或培训，我们不作这种宣传。

## 2. 它实际做什么

它把“解释一个知识点”与“持续带用户学会一个主题”分开：

1. **意图确认**：一次性问答正常回答，不强迫用户进入测验。
2. **诊断**：把主题拆成若干具体子技能，通过 3–5 个逐一提问定位起点。
3. **技能地图**：以 0–5 级显示状态；等级来自观察到的表现，而非用户自称或恭维。
4. **教学循环**：每次只问一个问题，等待回答；答错后聚焦误区，必要时再解释并换角度复测。
5. **证据门槛**：升级需要至少两次独立检查，其中包括不是刚看完答案的主动回忆。
6. **间隔复习与总评**：复测旧知识，最后混合考查子技能与综合应用。
7. **用户控制**：支持 `harder`、`easier`、`just tell me`、`save state` 和 `resume from:`。

`save state` 是输出可保存的文本，不是自动写入长期记忆数据库。
原始英文协议未被翻译覆盖或替换；本页是 P-Research 的说明，不是上游修改。

## 3. 为什么放入 P-Research

P-Research 重视可追溯、可评价的研究。这个技能提供一种值得检验的“学习反馈循环”：

```text
Research topic → diagnostic → subskills → questions → demonstrated answers
              → correction → delayed review → assessment → next topic
```

可尝试的用途包括论文方法理解、Python/SQL、概率统计、实验设计和研究技术答辩。
这些是**候选用途**，并未在本次导入中测得效果。

- 让“读过论文”与“能独立解释、复现并处理边界”分开。
- 把薄弱点、误解和下一次复测保存成明确状态。
- 为学习协议建立可观察的评价标准，而不只看回答是否流畅。

但“对话遵守协议”“答案正确”和“学习者真正掌握”是三种不同证据。
本次只验证源文件完整性和导入工程，不宣称它提升学习速度、记忆、研究产出或面试通过率。

## 4. 怎么使用

本仓库**没有把它自动安装到全局 Agent 或 Codex 配置**，也没有替换 P-Research 原管线。

手动试用时，可将原始 `SKILL.md` 提供给支持该格式的 Agent，并明确提出持续教学请求：

> 请使用这份 Socratic Tutor 协议教我 Python 字典。先逐题诊断，再给技能地图。
> 我希望最终能独立写代码并解释复杂度；不要因为我自称理解了就升级。

这是未执行的示例提示词，不是本仓库已有的学习结果。
如果要复制到其他工具的 skills 目录，需经过该工具正常的安装与权限流程，
同时携带上游 MIT 许可证与来源说明。宿主的安全、隐私和权限规则始终优先。
不要把客户资料、凭据、未公开研究或招聘沟通直接放入公共学习记录。

## 5. 结构与验证

```text
jane-street-socratic-tutor/
  upstream/                 # 六个原始 Git 文件，禁止混入本地说明
    socratic-tutor/SKILL.md
    LICENSE.md ...
  SOURCE_MANIFEST.json       # 提交、Git tree/blob、长度、SHA-256
  verify_snapshot.py        # stdlib-only、离线完整性校验
  EVALUATION_CASES.json      # 六类合成对话评价方案，尚未运行
  BENCHMARK_CARD.md          # 工程实测与学习效果的证据边界
  TEST_REPORT.md             # 观察到的测试、环境问题与限制
```

从仓库根目录执行：

```bash
python -X utf8 skills/jane-street-socratic-tutor/verify_snapshot.py
python -X utf8 -m unittest discover -s tests -p test_jane_street_socratic_tutor.py -v
```

校验器检查文件清单、长度、SHA-256、Git blob SHA 与完整 Git tree SHA。
它不是来源签名系统；可信来源仍需要从已审查的上游提交及版本历史确认。
也不是教学行为评测器，不能把完整性通过当成学习效果证明。

## 6. 下一步与维护规则

先固定模型/后端、对照提示词、题目集和人工评分规则，再做同模型 A/B。
[EVALUATION_CASES.json](EVALUATION_CASES.json) 提供固定的六类合成场景；目前行为、正确率、
延迟回忆、时间和 token 成本都为 `UNMEASURED`，没有调用付费模型。

后续若本地改进技能，放到独立 `experiments/`，标明相对上游的差异；不要改写
`upstream/` 冒充原作。更新上游时重新固定提交、审查许可与差异、生成清单并做树校验。
上游贡献另走其 DCO/Review 流程，不因为本地导入就默认有权代签或合并。
