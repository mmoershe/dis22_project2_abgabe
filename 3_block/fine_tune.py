import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
    from peft import LoraConfig, get_peft_model, TaskType
    from datasets import load_dataset

    import os

    os.putenv("HIP_VISIBLE_DEVICES", "0") 
    return (
        AutoModelForCausalLM,
        AutoTokenizer,
        LoraConfig,
        TaskType,
        Trainer,
        TrainingArguments,
        get_peft_model,
        load_dataset,
        os,
        torch,
    )


@app.cell
def _(torch):
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())
    print(torch.cuda.current_device())
    print(torch.cuda.get_device_name(torch.cuda.current_device()))
    return


@app.cell
def _(load_dataset, os):
    CURRENT_DIRECTORY: str = os.path.dirname(__file__)
    ROOT_DIRECTORY: str = os.path.dirname(CURRENT_DIRECTORY)
    DATA_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "data")
    cluster2_DIRECTORY: str = os.path.join(DATA_DIRECTORY, "cluster2.jsonl")
    model_DIRECTORY: str = os.path.join(DATA_DIRECTORY, "model-00002-of-00002.safetensors")

    assert os.path.exists(cluster2_DIRECTORY), f"Unable to find cluster2 at {cluster2_DIRECTORY = }"
    assert os.path.exists(model_DIRECTORY), f"Unable to find model at {model_DIRECTORY = }"

    dataset = load_dataset("json", data_files=cluster2_DIRECTORY, split="train")
    print(dataset)
    return (dataset,)


@app.cell
def _(AutoModelForCausalLM, AutoTokenizer, torch):
    # Load model and tokenizer
    # model_name = "NousResearch/Llama-2-7b-chat-hf" 
    model_name = "meta-llama/Llama-3.2-3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
    return model, tokenizer


@app.cell
def _(
    LoraConfig,
    TaskType,
    Trainer,
    TrainingArguments,
    dataset,
    get_peft_model,
    model,
    tokenizer,
):
    def preprocess(example):
        # Concatenate instruction and output as prompt + response
        text = example["instruction"] + example["output"]
        tokenized = tokenizer(
            text,
            truncation=True,
            max_length=512,
            padding="max_length"
        )
        # For causal LM, labels are usually the same as input_ids
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized

    tokenized_dataset = dataset.map(preprocess, batched=False)

    # LoRA configuration
    lora_config = LoraConfig(
        r=16,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )

    # Apply LoRA to the model
    lora_model = get_peft_model(model, lora_config)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./llama-lora-finetuned",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        num_train_epochs=2,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        save_steps=100,
        save_total_limit=2,
        report_to="none"
    )

    # Trainer
    trainer = Trainer(
        model=lora_model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
    )

    # Start fine-tuning
    trainer.train()
    return


if __name__ == "__main__":
    app.run()
