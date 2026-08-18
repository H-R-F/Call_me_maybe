# Pipeline Sequence

```mermaid
sequenceDiagram
    participant User as User
    participant Main as __main__.py
    participant CLI as cli.py
    participant Pipeline as pipeline.py
    participant IO as io_utils.py
    participant Schema as schema.py
    participant Model as Small_LLM_Model
    participant Decoder as decoder.py
    participant FS as JSON Files

    User->>Main: python -m src
    Main->>CLI: main()
    CLI->>CLI: _build_parser()
    CLI->>CLI: parse_args()
    CLI->>Pipeline: run_pipeline(fn_path, input_path, output_path)

    Pipeline->>IO: load_function_definitions(path)
    IO->>FS: read JSON
    FS-->>IO: raw data
    IO->>Schema: _validate_model(FunctionDefinition)
    Schema-->>IO: list[FunctionDefinition]
    IO-->>Pipeline: functions

    Pipeline->>IO: load_prompts(path)
    IO->>FS: read JSON
    FS-->>IO: raw data
    IO->>Schema: _validate_model(PromptItem)
    Schema-->>IO: list[PromptItem]
    IO-->>Pipeline: prompts

    Pipeline->>Model: Small_LLM_Model()
    Model->>Model: AutoTokenizer.from_pretrained()
    Model->>Model: AutoModelForCausalLM.from_pretrained()
    Model-->>Pipeline: model instance

    loop for each prompt
        Pipeline->>Decoder: decode(model, prompt, functions)

        Decoder->>Decoder: select_function_name()

        Decoder->>Decoder: _build_token_trie(functions, model)

        Decoder->>Model: encode(fn.name)
        Model-->>Decoder: token_ids

        Decoder->>Decoder: _build_token_trie()
        Decoder-->>Decoder: root TrieNode, mapping

        loop traverse trie
            Decoder->>Model: get_logits_from_input_ids(ids)
            Model-->>Decoder: next-token logits

            Decoder->>Decoder: _select_max_logit(logits, allowed)
            Decoder-->>Decoder: best token_id
        end

        Decoder->>Decoder: resolve function name
        Decoder-->>Decoder: name

        Decoder->>Decoder: _generate_parameters(prompt, function_def)
        Decoder->>Decoder: regex extraction
        Decoder-->>Decoder: parameters dict

        Decoder-->>Pipeline: DecodedCall {name, parameters}

        Pipeline->>Schema: OutputItem(prompt, name, parameters)
        Pipeline-->>Pipeline: collect OutputItem
    end

    Pipeline->>IO: write_output(path, items)
    IO->>Schema: item.model_dump()
    IO->>FS: write JSON
    IO-->>Pipeline: done

    Pipeline-->>CLI: list[dict]
    CLI-->>Main: return 0
    Main-->>User: exit
```

## Key Design Points

| Stage | Technique | Why |
|-------|-----------|-----|
| Function selection | Trie-constrained decoding | Only valid function names are generated — LLM can't hallucinate a wrong name |
| Parameter extraction | Regex + special handlers | Deterministic, no LLM calls needed for params |
| Model | Qwen3-0.6B | Lightweight, runs on CPU/MPS/CUDA |
| Validation | Pydantic BaseModel | Runtime type safety for JSON I/O |
