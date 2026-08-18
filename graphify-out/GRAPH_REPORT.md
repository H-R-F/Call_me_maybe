# Graph Report - .  (2026-06-14)

## Corpus Check
- Corpus is ~2,286 words - fits in a single context window. You may not need a graph.

## Summary
- 137 nodes · 202 edges · 10 communities (8 shown, 2 thin omitted)
- Extraction: 88% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Data Models & Schema|Data Models & Schema]]
- [[_COMMUNITY_Project Overview & Constraints|Project Overview & Constraints]]
- [[_COMMUNITY_CLI & Decoding Pipeline|CLI & Decoding Pipeline]]
- [[_COMMUNITY_Constrained Decoding Engine|Constrained Decoding Engine]]
- [[_COMMUNITY_LLM Model Wrapper|LLM Model Wrapper]]
- [[_COMMUNITY_Pydantic Data Models|Pydantic Data Models]]
- [[_COMMUNITY_CLI Entry Point|CLI Entry Point]]
- [[_COMMUNITY_LLM SDK Init|LLM SDK Init]]
- [[_COMMUNITY_Testing Framework|Testing Framework]]

## God Nodes (most connected - your core abstractions)
1. `FunctionDefinition` - 14 edges
2. `OutputItem` - 12 edges
3. `run_pipeline()` - 11 edges
4. `Small_LLM_Model` - 9 edges
5. `decode()` - 9 edges
6. `PromptItem` - 9 edges
7. `select_function_name()` - 8 edges
8. `_build_token_trie()` - 7 edges
9. `load_function_definitions()` - 7 edges
10. `load_prompts()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `TrieNode` --uses--> `FunctionDefinition`  [INFERRED]
  src/decoder.py → src/schema.py
- `DecodedCall` --uses--> `FunctionDefinition`  [INFERRED]
  src/decoder.py → src/schema.py
- `FunctionDefinition` --uses--> `FunctionDefinition`  [INFERRED]
  src/decoder.py → src/schema.py
- `Small_LLM_Model` --uses--> `FunctionDefinition`  [INFERRED]
  src/decoder.py → src/schema.py
- `Any` --uses--> `OutputItem`  [INFERRED]
  src/pipeline.py → src/schema.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Core source modules in src/ package** —  [EXTRACTED]
- **End-to-end pipeline: load -> decode -> write** —  [EXTRACTED]
- **Decoding subsystem: function selection + parameter extraction** —  [EXTRACTED]
- **Pydantic data models for input/output schema** —  [EXTRACTED]
- **Original subject authors/collaborators** —  [EXTRACTED]
- **Approved Python packages for the project** —  [EXTRACTED]
- **Quality assurance tools: linting, type checking, testing** —  [EXTRACTED]
- **LLM SDK wrapping Qwen3-0.6B for model inference** —  [EXTRACTED]
- **Hybrid approach: LLM-based function selection + deterministic parameter extraction** —  [EXTRACTED]

## Communities (10 total, 2 thin omitted)

### Community 0 - "Data Models & Schema"
Cohesion: 0.12
Nodes (31): BaseModel, ModelT, OutputItem, PromptItem, Pydantic validation framework, Pydantic model validation, load_function_definitions(), load_json_file() (+23 more)

### Community 1 - "Project Overview & Constraints"
Cohesion: 0.09
Nodes (25): 42 Curriculum, Call Me Maybe - 42 Project, Constrained Decoding, crfernan (collaborator), Graceful error handling, Flake8 linter, Function Calling in LLMs, ldevelle (collaborator) (+17 more)

### Community 2 - "CLI & Decoding Pipeline"
Cohesion: 0.10
Nodes (22): src/cli.py, decode(), DecodedCall TypedDict, src/decoder.py, Deterministic Parameter Extraction, Function Selection via LLM, _generate_parameters(), data/input/ directory (test inputs) (+14 more)

### Community 3 - "Constrained Decoding Engine"
Cohesion: 0.16
Nodes (20): Small_LLM_Model, _build_token_trie(), decode(), DecodedCall, _generate_parameters(), FunctionDefinition, Constrained decoding utilities., Generate parameters for the selected function. (+12 more)

### Community 4 - "LLM Model Wrapper"
Cohesion: 0.14
Nodes (7): dtype, Utility class wrapping a lightweight Hugging Face causal-LM for fast, low-memory, Tokenise *text* and return a 2-D ``input_ids`` tensor on the target device., Inverse of :py:meth:`encode`. Removes special tokens., Given a list of input token ids, return the raw logits (no softmax) for the next, Small_LLM_Model, Tensor

### Community 5 - "Pydantic Data Models"
Cohesion: 0.31
Nodes (9): FunctionDefinition Pydantic model, src/io_utils.py, load_function_definitions(), load_prompts(), OutputItem Pydantic model, ParameterSpec Pydantic model, PromptItem Pydantic model, src/schema.py (+1 more)

### Community 6 - "CLI Entry Point"
Cohesion: 0.32
Nodes (6): ArgumentParser, _build_parser(), main(), Command-line interface., Create the CLI argument parser., Run the CLI entry point.

## Ambiguous Edges - Review These
- `Call Me Maybe - 42 Project` → `<login1> (student author)`  [AMBIGUOUS]
   · relation: unknown

## Knowledge Gaps
- **2 isolated node(s):** `dtype`, `ArgumentParser`
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Call Me Maybe - 42 Project` and `<login1> (student author)`?**
  _Edge tagged AMBIGUOUS (relation: related to) - confidence is low._
- **Why does `FunctionDefinition` connect `Data Models & Schema` to `Constrained Decoding Engine`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `run_pipeline()` connect `Data Models & Schema` to `Constrained Decoding Engine`, `CLI Entry Point`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `FunctionDefinition` (e.g. with `ModelT` and `OutputItem`) actually correct?**
  _`FunctionDefinition` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `OutputItem` (e.g. with `ModelT` and `OutputItem`) actually correct?**
  _`OutputItem` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `dtype`, `Utility class wrapping a lightweight Hugging Face causal-LM for fast, low-memory`, `Tokenise *text* and return a 2-D ``input_ids`` tensor on the target device.` to the rest of the system?**
  _30 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Data Models & Schema` be split into smaller, more focused modules?**
  _Cohesion score 0.12477718360071301 - nodes in this community are weakly interconnected._