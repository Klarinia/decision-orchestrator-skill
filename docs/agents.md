# Agent & Prompt Specification

This document details the expected behavior for Router, Advisors, and CEO Final prompts.

## Router

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

## Advisors (Common Contract)

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

## CEO Final

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
