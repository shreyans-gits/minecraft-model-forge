# minecraft-model-forge 🧱

> Type a description. Get a Minecraft model.

`minecraft-model-forge` is a fine-tuned LLM pipeline that takes a plain English prompt — like `"a wooden dining chair"` or `"a medieval knight helmet"` — and outputs a valid Minecraft-compatible 3D model JSON file you can drop straight into your resource pack or mod.

---

## What this does

Minecraft models are just JSON files describing 3D cuboids — positions, sizes, and face mappings. This project treats that as a text generation problem.

We collect hundreds of real Minecraft model JSONs from:
- Minecraft's own asset files (blocks, entities)
- The MrCrayfish Furniture Mod
- Open-source Minecraft mods on CurseForge and GitHub

We then fine-tune a small open-source language model (GPT-2 or TinyLlama) on those files using HuggingFace Transformers, training it to map descriptions to geometry. The result is a pipeline where a prompt produces a ready-to-use `.json` model file.

---

## Pipeline overview

```
Text prompt
    ↓
Fine-tuned LLM (GPT-2 / TinyLlama)
    ↓
Raw JSON output
    ↓
Validation + cleanup
    ↓
model.json  ← drop into your resource pack
```

---

## Project structure

```
minecraft-model-forge/
│
├── data/
│   ├── raw/                  # Collected .json model files from all sources
│   └── processed/            # Cleaned, normalized, training-ready examples
│
├── scripts/
│   ├── filter.py             # Remove invalid or unusable model files
│   ├── normalize.py          # Standardize structure across sources
│   ├── build_dataset.py      # Format prompt→model training pairs
│   └── validate_output.py    # Check generated JSON is valid Minecraft geometry
│
├── training/
│   └── finetune.ipynb        # Google Colab fine-tuning notebook
│
├── inference/
│   └── generate.py           # Run a prompt through the model, output a .json file
│
└── README.md
```

---

## Goals

- [x] Define project scope and pipeline
- [ ] Collect and clean dataset (Minecraft assets + mods)
- [ ] Preprocess into prompt→model training pairs
- [ ] Fine-tune LLM on Google Colab
- [ ] Build inference script (prompt → `.json`)
- [ ] Add texture application layer

---

## Stack

| Tool | Purpose |
|---|---|
| HuggingFace Transformers | Model loading and fine-tuning |
| Google Colab | Free GPU training |
| GPT-2 / TinyLlama | Base model |
| Python | Everything else |

---

## Future plans

- Texture application — map description keywords to Minecraft textures and inject them into the output
- Simple web UI for non-technical users
- Support for animated models (`.bbmodel` format)

---

## Built by

Krish — part of a hands-on ML learning journey, building real projects from scratch.
