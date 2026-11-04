# 活动策划天团（campus-event-planner）

多角色协同的活动策划专家团：输入活动基本信息（名称、类型、规模、日期、场地），并行产出策划方案、预算、风险预案与宣传文案，最终汇编为一份完整的 HTML 策划方案，并附预算 Excel、风险预案 Excel、宣传 PPTX 三份附件。

## 类型

Team 型（多角色协作团队）· 分类：09-OperationsHR（运营人力）

## 团队成员

| Agent ID | 名字 | 职业 | 负责段落 |
|---|---|---|---|
| campus-event-planner-team-lead | 周全成 | 策划总监 | 编排调度、交叉核对、整合输出 |
| proposal-writer | 陈述之 | 方案主笔 | 一主题 / 二背景意义 / 三时间 / 四参与人员 / 五内容与流程 / 八总纲 |
| logistics-coordinator | 彭备齐 | 后勤筹备官 | 六活动准备（物料、场地、分工与联系方式） |
| budget-analyst | 钱算清 | 预算分析师 | 七活动预算（项目/数量/单价/总价/合计）+ 预算 Excel |
| risk-manager | 卫平安 | 风险管控师 | 八注意事项深化（风险分级与应急）+ 风险预案 Excel |
| promo-copywriter | 宣达远 | 宣传文案师 | 宣传文案 + 宣传 PPTX |

## 工作流程（SOP）

- **Phase 1（并行）**：主理人确认活动五要素 → TeamCreate → 同时调度五位团员各自独立产出。
- **Phase 2（串行）**：主理人回收五份产出，核对金额、时间、地点一致性，汇编为八段式 HTML 策划方案并附三份附件。

## 内置技能

`skills/event-planning-kit` — 固化「策划书八段式」「预算表」「风险预案」「宣传文案」四套模板，统一全团产出格式。

## 使用示例

- 帮我策划一场社团迎新破冰活动，规模 80 人，下周五晚 7 点在大学生活动中心多功能厅，要完整策划书、预算、风险预案和宣传文案。
- 给一场讲座活动做一份详细预算表，列出场地、物料、餐饮、奖品等支出项目与单价合计。
- 为我的活动写一版面向大一新生的宣传推送文案和海报文案，风格活泼有网感。

## 头像

头像位于 `avatars/`，当前为本地生成的品牌占位图（深蓝灰底 + 姓名/职能）。可直接替换为真人插画风格，要求：

- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB
- 建议风格：统一漫画/插画风，灰蓝（navy slate-blue）背景

## 安装

专家包目录已注册，路径：

```
C:\Users\lenovo\.workbuddy-ai\plugins\marketplaces\my-experts\plugins\campus-event-planner
```

如需在其他机器安装，将包放入同级目录后执行：

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
python3 scripts/package_expert.py <expert-dir> <output-dir>
```
