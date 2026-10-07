"""Convert nested dual-triple records to linked, flat training triples."""

import argparse
import json
from pathlib import Path


def flatten_graph(graph):
    if not isinstance(graph, dict):
        raise ValueError("Expected a dictionary of categories and relations.")
    triples = []
    for category, relations in graph.items():
        if not isinstance(relations, dict):
            raise ValueError(f"Invalid relations in category {category!r}.")
        for relation, entries in relations.items():
            if not isinstance(entries, list):
                raise ValueError(f"Expected an entry list for {category}/{relation}.")
            for index, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    raise ValueError(f"Invalid record at {category}/{relation}/{index}.")
                for field in ("Head", "Tail"):
                    if not isinstance(entry.get(field), str) or not entry[field].strip():
                        raise ValueError(f"Missing {field} at {category}/{relation}/{index}.")
                pair_id = f"{category}/{relation}/{index}"
                triples.append({
                    "Head": entry["Head"], "Relation": relation, "Tail": entry["Tail"],
                    "Category": category, "Pair ID": pair_id, "Triple Type": "predefined",
                })
                dynamic_fields = ("Dynamic Relation", "Additional Tail")
                if any(field in entry for field in dynamic_fields):
                    for field in dynamic_fields:
                        if not isinstance(entry.get(field), str) or not entry[field].strip():
                            raise ValueError(f"Missing {field} at {pair_id}.")
                    triples.append({
                        "Head": entry["Tail"], "Relation": entry["Dynamic Relation"],
                        "Tail": entry["Additional Tail"], "Category": category,
                        "Pair ID": pair_id, "Triple Type": "dynamic",
                    })
    return triples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("example.json"))
    parser.add_argument("--output", type=Path, default=Path("example_triples.json"))
    args = parser.parse_args()
    with args.input.open(encoding="utf-8") as handle:
        triples = flatten_graph(json.load(handle))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(triples, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Wrote {len(triples)} linked triples to {args.output}")


if __name__ == "__main__":
    main()
