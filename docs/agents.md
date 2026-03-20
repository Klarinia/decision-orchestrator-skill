# Agent & Prompt Specification

This document defines output contracts for Router, Advisors, and CEO Final.

## Router / 路由器

### Inputs
- objective
- context
- constraints
- success metrics

### Output Keys
- category
- confidence
- route
- data_gaps
- handoff_notes

### Quality Rules
- Must route to one of the allowed chains.
- Must report missing data when confidence is not high.

## Advisors / 顾问层 (Common Contract)

### Mandatory Output Blocks
- decision
- scores
- reasons
- risks
- missing_data
- action_48h

### Scoring
0-5 scale per dimension.

### Hard Stops
Each advisor must explicitly mark blocking conditions.

## Advisor Names (EN / 中文)
- Drucker / 德鲁克
- Jobs / 乔布斯
- Kenya Hara / 原研哉
- Munger / 芒格
- Buffett / 巴菲特
- Musk / 马斯克

## CEO Final / 最终拍板层

### Mandatory Output Blocks
- final_decision
- why
- conflicts
- rejected_options
- action_48h
- action_7d
- kill_criteria
- review_date

### Decision Discipline
- Explicit tradeoff statement is required.
- Action owner and deadline are required.
