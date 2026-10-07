# DYNA-SKILL

**Dynamic Self-Prompting Knowledge Graphs for Improving Logical Reasoning in Language Models**

[![Paper](https://img.shields.io/badge/Paper-IEEE_Access_2025-00629B)](https://doi.org/10.1109/ACCESS.2025.3626479)

**Jongwon Ryu, Mingi Kim, and Junyeong Kim**

Research code for constructing and processing the self-prompted knowledge graphs
introduced in [the paper](https://doi.org/10.1109/ACCESS.2025.3626479).

## Overview

DYNA-SKILL links predefined commonsense relations with context-dependent relations
generated through self-prompting. Each record connects two triples:

```text
Head -- Predefined Relation --> Tail -- Dynamic Relation --> Additional Tail
```

The paper combines 35 predefined relations with 133 dynamic relations. This
repository releases the graph-generation prompts and data-processing scripts;
the complete generated corpus, fine-tuning/evaluation code, and model checkpoints
are not included.

## Setup

Use Python 3.10 or 3.11 and an isolated environment:

```bash
git clone https://github.com/jongwonryu/dyna-skill.git
cd dyna-skill
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The research scripts use `openai==0.28.1`, which supports their original
`ChatCompletion` interface. Configure credentials through the environment,
not by editing source files:

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
export OPENAI_MODEL="gpt-4-turbo"
python scripts/check_api.py
```

`gpt-4-turbo` is the historical model default, not a guarantee of current account
availability. Set `OPENAI_MODEL` to an accessible Chat Completions model with
compatible parameters. The API check and generation scripts make paid requests;
changing models may change the generated data and does not reproduce the original
paper's results.

## Pipeline

Run commands from the repository root. The generation prompts and head categories
are defined in `scripts/generate_graph.py`.

```bash
# Generate nested dual-triple records. Review the scope before starting:
# the full configuration makes many paid API requests.
python scripts/generate_graph.py

# Split each record into predefined and dynamic triples, preserving pair IDs.
python scripts/flatten_graph.py --input example.json --output example_triples.json

# Apply the original relation-frequency filtering and sentence templates.
python scripts/clean_relations.py
python scripts/triples_to_text.py
```

| Stage | Input | Output |
| --- | --- | --- |
| Graph generation | Head categories and relation prompts | `example.json` |
| Flattening | `example.json` | `example_triples.json` |
| Relation cleaning | `example_triples.json` | `cleaned_triples.json` |
| Text conversion | `cleaned_triples.json` | `converted_text_data.txt` |

`scripts/extend_tails.py` is an optional legacy expansion stage. It reads
`example.json` and writes `example_updated.json`; pass that output to the flattening
script if using the expanded records. The original cleaning rule retains relations
whose raw label occurs **more than 10 times**, then removes punctuation.

Generation scripts write progress files in the working directory. They are
research utilities, not a transactional job system: retain backups of outputs
and state before rerunning an interrupted generation job.

## Data Format

The generated JSON groups records by category and predefined relation:

```json
{
  "Social-Interaction Relations": {
    "xIntent": [
      {
        "Head": "A person studies for an exam",
        "Tail": "To understand the course material",
        "Dynamic Relation": "Supports",
        "Additional Tail": "Preparing a study plan"
      }
    ]
  }
}
```

This schema example explains the format; it is not a released experimental sample.
Flattened records use `Head`, `Relation`, and `Tail`, plus `Category`, `Pair ID`,
and `Triple Type` so the two linked triples can be traced back to their source.

## Citation

```bibtex
@article{ryu2025dynaskill,
  title   = {{DYNA-SKILL}: Dynamic Self-Prompting Knowledge Graphs for Improving Logical Reasoning in Language Models},
  author  = {Ryu, Jongwon and Kim, Mingi and Kim, Junyeong},
  journal = {IEEE Access},
  volume  = {13},
  pages   = {188326--188334},
  year    = {2025},
  doi     = {10.1109/ACCESS.2025.3626479}
}
```

## Contact

Jongwon Ryu: `fbwhddnjs511@cau.ac.kr`.

No software license has been specified for this repository; the paper's publication
license does not automatically license the code.
