---
type: community
members: 21
---

# Constrained Decoding Engine

**Members:** 21 nodes

## Members
- [[Build a token-id trie for function names.]] - rationale - src/decoder.py
- [[Constrained decoding utilities.]] - rationale - src/decoder.py
- [[Convert tensor-like outputs to a flat list of ints.]] - rationale - src/decoder.py
- [[Decode a constrained function call (name + parameters).]] - rationale - src/decoder.py
- [[Decoded function call data with parameters.]] - rationale - src/decoder.py
- [[DecodedCall]] - code - src/decoder.py
- [[FunctionDefinition]] - code - src/decoder.py
- [[Generate parameters for the selected function.]] - rationale - src/decoder.py
- [[Pick the best function name using the LLM scores.]] - rationale - src/decoder.py
- [[Pick the token id with highest logit among allowed ids.]] - rationale - src/decoder.py
- [[Small_LLM_Model_1]] - code - src/decoder.py
- [[Token-id trie node for constrained name decoding.]] - rationale - src/decoder.py
- [[TrieNode]] - code - src/decoder.py
- [[TypedDict]] - code
- [[_build_token_trie()]] - code - src/decoder.py
- [[_generate_parameters()]] - code - src/decoder.py
- [[_select_max_logit()]] - code - src/decoder.py
- [[_tensor_to_ids()]] - code - src/decoder.py
- [[decode()]] - code - src/decoder.py
- [[decoder.py]] - code - src/decoder.py
- [[select_function_name()]] - code - src/decoder.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Constrained_Decoding_Engine
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Data Models & Schema]]

## Top bridge nodes
- [[decoder.py]] - degree 12, connects to 1 community
- [[decode()]] - degree 9, connects to 1 community
- [[DecodedCall]] - degree 5, connects to 1 community
- [[FunctionDefinition]] - degree 5, connects to 1 community
- [[Small_LLM_Model_1]] - degree 5, connects to 1 community