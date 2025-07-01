import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import torch
    from datasets import load_dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
    from peft import LoraConfig
    from trl import SFTTrainer, SFTConfig

    import os
    return (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        LoraConfig,
        SFTConfig,
        SFTTrainer,
        TrainingArguments,
        load_dataset,
        os,
        torch,
    )


@app.cell
def _(load_dataset, os):
    CURRENT_DIRECTORY: str = os.path.dirname(__file__)
    ROOT_DIRECTORY: str = os.path.dirname(CURRENT_DIRECTORY)
    DATA_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "data")
    cluster2_DIRECTORY: str = os.path.join(DATA_DIRECTORY, "cluster2.jsonl")

    assert os.path.exists(cluster2_DIRECTORY), f"Unable to find cluster2 at {cluster2_DIRECTORY = }"

    dataset = load_dataset("json", data_files=cluster2_DIRECTORY, split="train")
    return (dataset,)


@app.cell
def _(AutoTokenizer):
    # Model and tokenizer
    base_model_name = "NousResearch/Llama-2-7b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return (base_model_name,)


@app.cell
def _(BitsAndBytesConfig, torch):
    # QLoRA quantization config
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )
    return


@app.cell
def _(AutoModelForCausalLM, base_model_name, torch):
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        # quantization_config=quant_config,
        device_map="auto", 
        torch_dtype=torch.float16
    )
    model.config.use_cache = False
    return (model,)


@app.cell
def _(LoraConfig):
    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    return (lora_config,)


@app.cell
def _(TrainingArguments):
    training_args = TrainingArguments(
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=True,
        output_dir="./output",
    )
    return


@app.cell
def _(SFTConfig):
    sft_config = SFTConfig(
        output_dir="./output",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=True,
        dataset_text_field="text",  # <-- SFT-specific!
        max_seq_length=512,         # <-- SFT-specific!
        packing=False
    )
    return (sft_config,)


@app.cell
def _(SFTTrainer, dataset, lora_config, model, sft_config):
    # If your dataset has "instruction" and "output", combine them:
    def formatting_func(example):
        return f"Instruction: {example['instruction']}\nOutput: {example['output']}"

    # Add a "text" field to your dataset
    formatted_dataset = dataset.map(lambda x: {"text": formatting_func(x)})
    trainer = SFTTrainer(
        model=model,
        train_dataset=formatted_dataset,
        args=sft_config,
        peft_config=lora_config,
    )

    trainer.train()
    return


if __name__ == "__main__":
    app.run()
