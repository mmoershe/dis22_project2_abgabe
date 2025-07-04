import os
import json

CURRENT_DIR: str = os.path.dirname(__file__)
SUBMISSIONS_DIRECTORIES: list[str] = ["1_frage", "2_filter", "3_block"]

TEAM_NAME: str = "The Query Lab"

for submission_dir in SUBMISSIONS_DIRECTORIES:
    output_dir: str = os.path.join(CURRENT_DIR, submission_dir, "output")
    json_dir: str = os.path.join(CURRENT_DIR, submission_dir, "run_file.json")

    assert os.path.exists(output_dir), (
        f"Couldn't find Output Directory at {output_dir = }"
    )

    all_output_files: list[str] = os.listdir(output_dir)
    all_queries_files: list[str] = [
        file for file in all_output_files if file.endswith(".queries")
    ]

    if submission_dir == "1_frage":
        metadata: dict = {
            "team_name": TEAM_NAME,
            "approach_description": "sophisticated questions generator based off of human question characteristics",
            "task": "Task_A1",
            "run_name": "weighted_question",
        }

    if submission_dir == "2_filter":
        metadata: dict = {
            "team_name": TEAM_NAME,
            "approach_description": "Llama finetuned on human filter method",
            "task": "Task_A1",
            "run_name": "finetuned_llm_filter",
        }

    if submission_dir == "3_block":
        metadata: dict = {
            "team_name": TEAM_NAME,
            "approach_description": "Llama finetuned on human boolean block method",
            "task": "Task_A1",
            "run_name": "finteund_llm_block",
        }

    run_file: dict = dict()

    for queries_file in all_queries_files:
        index: int = int(queries_file.split("-")[2])
        queries_file_dir: str = os.path.join(output_dir, queries_file)
        with open(queries_file_dir, "r") as file:
            lines = [line.strip() for line in file][1::]
        run_file[int(index)] = lines

    sorted_dict = dict(sorted(run_file.items()))

    sorted_dict = {"meta": metadata, **sorted_dict}

    string_key_dict = {str(k): v for k, v in sorted_dict.items()}

    with open(json_dir, "w") as f:
        json.dump(string_key_dict, f, indent=4)
