{
  "type": "excalidraw",
  "version": 2,
  "source": "decoder_explanation",
  "elements": [
    {
      "type": "text",
      "version": 1,
      "x": 250,
      "y": 20,
      "width": 600,
      "height": 30,
      "text": "🧠 decoder.py — Constrained Function Call Engine",
      "fontSize": 22,
      "textAlign": "center",
      "id": "title"
    },

    {
      "type": "rectangle",
      "x": 40,
      "y": 80,
      "width": 300,
      "height": 120,
      "strokeColor": "#58a6ff",
      "backgroundColor": "#161b22",
      "id": "input_box"
    },
    {
      "type": "text",
      "x": 55,
      "y": 90,
      "width": 280,
      "height": 100,
      "text": "📥 INPUT\n\nprompt\nfunctions list\nmodel (Small_LLM_Model)\n\n→ raw natural language",
      "fontSize": 12,
      "id": "input_text"
    },

    {
      "type": "rectangle",
      "x": 380,
      "y": 80,
      "width": 320,
      "height": 120,
      "strokeColor": "#7ee787",
      "backgroundColor": "#0d1117",
      "id": "select_fn_box"
    },
    {
      "type": "text",
      "x": 395,
      "y": 90,
      "width": 300,
      "height": 100,
      "text": "🎯 STEP 1: select_function_name()\n\n• build prompt context\n• encode prompt → tokens\n• build Trie of valid names\n• constrained decoding (logits)\n→ outputs VALID function name",
      "fontSize": 12,
      "id": "select_fn_text"
    },

    {
      "type": "rectangle",
      "x": 750,
      "y": 80,
      "width": 300,
      "height": 120,
      "strokeColor": "#f0883e",
      "backgroundColor": "#0d1117",
      "id": "function_box"
    },
    {
      "type": "text",
      "x": 765,
      "y": 90,
      "width": 280,
      "height": 100,
      "text": "⚙️ OUTPUT (STEP 1)\n\nfunction name\n→ e.g. fn_greet\n\npicked via Trie + logits\n(no invalid names possible)",
      "fontSize": 12,
      "id": "function_text"
    },

    {
      "type": "rectangle",
      "x": 380,
      "y": 240,
      "width": 320,
      "height": 160,
      "strokeColor": "#ffa657",
      "backgroundColor": "#0d1117",
      "id": "param_box"
    },
    {
      "type": "text",
      "x": 395,
      "y": 250,
      "width": 300,
      "height": 140,
      "text": "🧩 STEP 2: _generate_parameters()\n\nRULE-BASED EXTRACTION:\n• regex numbers\n• detect quotes\n• detect booleans\n• special logic per function\n\n→ NO AI here\n→ pure heuristics",
      "fontSize": 12,
      "id": "param_text"
    },

    {
      "type": "rectangle",
      "x": 750,
      "y": 240,
      "width": 300,
      "height": 160,
      "strokeColor": "#d2a8ff",
      "backgroundColor": "#0d1117",
      "id": "final_box"
    },
    {
      "type": "text",
      "x": 765,
      "y": 250,
      "width": 280,
      "height": 140,
      "text": "📦 FINAL OUTPUT (decode)\n\n{\n  name: \"fn_greet\",\n  parameters: {...}\n}\n\n→ DecodedCall TypedDict\n→ ready for pipeline",
      "fontSize": 12,
      "id": "final_text"
    },

    {
      "type": "rectangle",
      "x": 40,
      "y": 240,
      "width": 300,
      "height": 160,
      "strokeColor": "#f85149",
      "backgroundColor": "#161b22",
      "id": "model_box"
    },
    {
      "type": "text",
      "x": 55,
      "y": 250,
      "width": 280,
      "height": 140,
      "text": "🤖 Small_LLM_Model\n\n• encode(text)\n• decode(ids)\n• get_logits(...)\n\n→ brain behind selection\n→ produces token probabilities",
      "fontSize": 12,
      "id": "model_text"
    },

    {
      "type": "arrow",
      "x": 340,
      "y": 140,
      "width": 40,
      "height": 0,
      "strokeColor": "#58a6ff",
      "id": "arrow1"
    },
    {
      "type": "arrow",
      "x": 700,
      "y": 140,
      "width": 40,
      "height": 0,
      "strokeColor": "#7ee787",
      "id": "arrow2"
    },
    {
      "type": "arrow",
      "x": 560,
      "y": 200,
      "width": 0,
      "height": 40,
      "strokeColor": "#ffa657",
      "id": "arrow3"
    },
    {
      "type": "arrow",
      "x": 700,
      "y": 320,
      "width": 40,
      "height": 0,
      "strokeColor": "#d2a8ff",
      "id": "arrow4"
    }
  ],
  "appState": {
    "theme": "dark",
    "viewBackgroundColor": "#0d1117"
  }
}