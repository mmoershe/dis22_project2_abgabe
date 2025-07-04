# Submission 3 - Finetuned Block LLM

## Files

| File/Directory                | Description                                                                   |
| ----------------------------- | ----------------------------------------------------------------------------- |
| `run_file.json`               | run_file for this submission generated using the script in the root directory |
| `./output/*`                  | output files copied from Sim4IA, used for the run_files                       |
| `fine_tune.py`                | notebook used for fine tuning local LLM (**Marimo**)                          |
| `finetuned_block_strategy.py` | query generator used                                                          |
| `use_model.py`                | notebook used for testing the finetuned combined model (**Marimo**)           |

## Lab Note

**Team name**: The Query Lab  
**Members**: Mark Henri Mörsheim, Maryam El Ghadioui

After removing bot users, another group identified and clustered three types of real users. One of them were users, who used rather elaborate "Boolean Block Queries". Simulating these users was our goal with this submission. Here's an example of what this type of user may use as a query:

```txt
("climate change" OR "global warming" OR "climate crisis") AND ("social media" OR Twitter OR Facebook OR Instagram) AND ("misinformation" OR "public opinion" OR "awareness") NOT ("renewable energy" OR "solar power" OR "wind energy")
```

We used an LLM approach to contrast our first submission, and because this type of query seems to be fitting for an LLM, but because of the private nature of our real user data, using an external service was not an option.
Luckily, fine-tuned smaller (local) LLMs can often compete or even outperform large generic models for very specific tasks, obviously depending on the task and training data.
This is a great way to balance the inferior hardware at hand.

Training and generation was done on an **AMD RX 7800XT (_16GB of Vram_)** on **Arch Linux** / **Ubuntu 24.04.02**, using **ROCm 6.4** and the **PyTorch Nightly** version to match the ROCm version.
We used Meta's **Llama3.2 (3B)** as our base model, because it's relatively new, very small in size, yet powerful (enough).

The cluster of queries we trained our model on had to be converted to a "question-answer" structure.
This way a _Keyphrase_ was introduced in training, which the model recognizes before generating an answer that is based on the LoRA training.
This is the reason our prompt is structured like this:

```python
prompt: str = f"{query}. {keyphrase}"
```

```txt
# Example Prompt:
climate change misinforatmion wildfires. Output:
```

