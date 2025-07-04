import os
import json

CURRENT_DIR: str = os.path.dirname(__file__)
OUTPUT_DIR: str = os.path.join(CURRENT_DIR, "output")
JSON_DIR: str = os.path.join(CURRENT_DIR, "run_file.json")

assert os.path.exists(OUTPUT_DIR), f"Couldn't find Output Directory at {OUTPUT_DIR = }"


all_output_files: list[str] = os.listdir(OUTPUT_DIR)
all_queries_files: list[str] = [
    file for file in all_output_files if file.endswith(".queries")
]

metadata: dict = {
    "team_name": "MaRi",
    "approach_description": "Llama finetuned on human boolean block method",
    "task": "Task_A1",
    "run_name": "llm_block",
}

run_file: dict = dict()

for queries_file in all_queries_files:
    index: int = int(queries_file.split("-")[2])
    queries_file_dir: str = os.path.join(OUTPUT_DIR, queries_file)
    with open(queries_file_dir, "r") as file:
        lines = [line.strip() for line in file][1::]
    run_file[int(index)] = lines

sorted_dict = dict(sorted(run_file.items()))

sorted_dict = {"meta": metadata, **sorted_dict}

string_key_dict = {str(k): v for k, v in sorted_dict.items()}

with open(JSON_DIR, "w") as f:
    json.dump(string_key_dict, f, indent=4)
