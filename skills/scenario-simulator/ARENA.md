# Arena — scenario-simulator
# Human edits this. The organism runs experiments against it overnight.
# Analogous to program.md in Karpathy's autoresearch.

## Fitness metric
primary: composite_score
formula: "persona_diversity×0.25 + counterfactual_plausibility×0.25 + deliberation_depth×0.20 + output_clarity×0.20 + safety_compliance×0.10"
improvement_threshold: 0.05
regression_threshold: 0.10

## Experiment budget
eval_budget_seconds: 45
eval_dataset: "datasets/synthetic/scenario-simulator/shard_000.json"
eval_n_items: 40
max_experiments_per_generation: 12

## Mutation strategies
allowed_mutations:
  - persona_diversity_expansion
  - counterfactual_branching_depth
  - deliberation_round_structure
  - output_schema_tightening
  - edge_case_handling
  - convergence_detection_tuning

## Transfer test (Karpathy's depth-N insight applied to skill complexity)
transfer_dataset: "datasets/synthetic/scenario-simulator/shard_001.json"
transfer_n_items: 30
transfer_pass_threshold: -0.15

## Browser arena config
browser_demo_enabled: true
demo_eval_dimensions: [persona_diversity, counterfactual_plausibility, deliberation_depth, output_clarity, safety_compliance]

## Trilogy integration
mindspider_feed_enabled: false
bettafish_engine_type: null
mirofish_simulation_enabled: true

## What "better" means
improvement_requires:
  - composite_score increases by >= 0.05
  - safety_compliance does NOT decrease
  - transfer_test passes
notes: "Better = more diverse agent perspectives, more plausible counterfactual branches, clearly marked as simulation."
