# Pipeline Flow

```mermaid
flowchart TB
    subgraph CLI[CLI Layer]
        direction TB
        ENTRY["python -m src<br/>__main__.py"] --> CLI_MAIN["cli.main()"]
        CLI_MAIN --> PARSE["_build_parser()<br/>args: --functions_definition<br/>--input --output"]
    end

    subgraph IO[I/O Layer - io_utils.py]
        direction TB
        LOAD_FN["load_function_definitions()<br/>Reads JSON, validates"] --> VAL_FN["_validate_model()<br/>Pydantic: FunctionDefinition"]
        LOAD_P["load_prompts()<br/>Reads JSON, validates"] --> VAL_P["_validate_model()<br/>Pydantic: PromptItem"]
        WRITE["write_output()<br/>Dumps OutputItems → JSON"]
    end

    subgraph MODEL[Model Layer - llm_sdk]
        LLM["Small_LLM_Model()<br/>Loads Qwen3-0.6B<br/>from HuggingFace"]
        ENC["encode(text) → token_ids"]
        DEC["decode(ids) → text"]
        LOGITS["get_logits_from_input_ids()<br/>→ next-token logits"]
    end

    subgraph DECODER[Decoder - decoder.py]
        direction TB
        DECODE_MAIN["decode()"]
        SELECT_FN["select_function_name()"]
        BUILD_TRIE["_build_token_trie()<br/>Builds TrieNode of<br/>function name token IDs"]
        SELECT_LOGIT["_select_max_logit()<br/>Picks highest-logit<br/>allowed token"]
        GEN_PARAMS["_generate_parameters()"]
        EXTRACT_NUM["Extract numbers<br/>via regex"]
        EXTRACT_STR["Extract strings<br/>via regex"]
        EXTRACT_BOOL["Extract booleans<br/>via keywords"]
        EXTRACT_GREET["extract_greet_name()<br/>Special handler"]
        EXTRACT_SUBST["extract_substitution()<br/>Special handler"]
    end

    subgraph SCHEMA[Schema Layer - schema.py]
        FD["FunctionDefinition<br/>Pydantic BaseModel"]
        PS["ParameterSpec<br/>Pydantic BaseModel"]
        PI["PromptItem<br/>Pydantic BaseModel"]
        OI["OutputItem<br/>Pydantic BaseModel"]
    end

    subgraph DATA[Data Files]
        FD_JSON["data/input/<br/>functions_definition.json"]
        INPUT_JSON["data/input/<br/>function_calling_tests.json"]
        OUTPUT_JSON["data/output/<br/>function_calling_results.json"]
    end

    ENTRY --> CLI_MAIN
    CLI_MAIN --> PARSE
    PARSE --> LOAD_FN
    PARSE --> LOAD_P
    LOAD_FN --> FD_JSON
    LOAD_P --> INPUT_JSON
    LOAD_FN --> FD
    LOAD_P --> PI
    PI --> DECODE_MAIN
    FD --> DECODE_MAIN
    LLM --> DECODE_MAIN
    DECODE_MAIN --> SELECT_FN
    DECODE_MAIN --> GEN_PARAMS
    SELECT_FN --> BUILD_TRIE
    BUILD_TRIE --> ENC
    BUILD_TRIE --> SELECT_LOGIT
    SELECT_LOGIT --> LOGITS
    GEN_PARAMS --> EXTRACT_NUM
    GEN_PARAMS --> EXTRACT_STR
    GEN_PARAMS --> EXTRACT_BOOL
    GEN_PARAMS --> EXTRACT_GREET
    GEN_PARAMS --> EXTRACT_SUBST
    EXTRACT_GREET --> PI
    EXTRACT_SUBST --> PI
    DECODE_MAIN --> OI
    OI --> WRITE
    WRITE --> OUTPUT_JSON
```

## Step-by-step

1. **CLI** parses 3 JSON paths (functions definition, input prompts, output)
2. **Load** function definitions & prompts from `data/input/`, validated via Pydantic schemas
3. **Init** `Small_LLM_Model` — downloads Qwen3-0.6B from HuggingFace
4. **For each prompt:**
   - **`select_function_name()`** — builds a token-ID trie of function names, walks it constrained: at each step only valid next tokens (trie children) are allowed, picks the highest logit
   - **`_generate_parameters()`** — extracts numbers/strings/booleans via regex, with special handlers for `fn_greet` and `fn_substitute_string_with_regex`
5. **Write** `OutputItem` results to `data/output/function_calling_results.json`

## Communities

- [[_COMMUNITY_CLI & Decoding Pipeline]]
- [[_COMMUNITY_Constrained Decoding Engine]]
- [[_COMMUNITY_Data Models & Schema]]
- [[_COMMUNITY_LLM Model Wrapper]]
- [[_COMMUNITY_Project Overview & Constraints]]
