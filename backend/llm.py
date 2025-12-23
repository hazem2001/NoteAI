from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen2.5-3B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    load_in_4bit=True,
    device_map="auto",
    offload_folder="./llmOffload",           
    torch_dtype="auto"            
)

tokenizer = AutoTokenizer.from_pretrained(model_id)

# If tokens exceed 2k, we drop them. Later, we can batch them.
def query_notes(notes, query):
    prompt = f"Instruction : {query}\nInput:\n"
    for i, note in enumerate(notes):
        prompt += f"{i + 1}) Title: {note.title} \n Content: {note.content} \n"
    prompt += "Answer: "

    inputs = tokenizer(prompt, return_tensors="pt", max_length=2000, truncation=True).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        do_sample=True,
        top_p=0.7
    )

    generated_tokens_only = outputs[0][inputs["input_ids"].shape[1]:]

    text = tokenizer.decode(generated_tokens_only, skip_special_tokens=True)
    print(text, len(outputs[0]))
    return text



