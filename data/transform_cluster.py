import pandas as pd
import os
import json


CURRENT_DIRECTORY: str = os.path.dirname(__file__)


possible_cluster_files: list[str] = ["cluster1.tsv", "cluster2.tsv", "cluster3.tsv"]
for cluster_file in possible_cluster_files:
    if cluster_file not in os.listdir(CURRENT_DIRECTORY):
        continue

    data: pd.DataFrame = pd.read_csv(
        os.path.join(CURRENT_DIRECTORY, cluster_file), delimiter="\t"
    )
    queries: pd.Series = pd.Series(data["query"])
    # formatted_lines = queries.apply(
    #     lambda x: f"<s>[INST] Generate output: [/INST] {x} </s>"
    # )
    formatted_lines = queries.apply(
        lambda x: "{" + f'"Instruction": "Output:", "output": "{x}"' + "}"
    )

    filename: str = cluster_file.replace(".tsv", ".jsonl")
    # formatted_lines.to_csv(filename, index=False, header=False)

    # with open(filename, "w", encoding="utf-8") as f:
    #     for line in formatted_lines:
    #         f.write(line + "\n")

    with open(filename, "w", encoding="utf-8") as f:
        for x in queries:
            obj = {"instruction": "Output:", "output": x}
            f.write(json.dumps(obj, ensure_ascii=True) + "\n")
