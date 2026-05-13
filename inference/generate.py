import torch
import json
import os
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def load_model(model_path):
    base_model_id = "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T"
    
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        dtype=torch.float16,
        device_map="auto" 
    )
    model = PeftModel.from_pretrained(base_model, model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model.eval()
    return model, tokenizer

def generate(prompt, model, tokenizer, max_new_tokens=1024):
    formatted_prompt = f"[NAME]: {prompt}\n[MODEL]:"
    
    device = next(model.parameters()).device
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)
    
    with torch.no_grad():
        output_tokens = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    return tokenizer.decode(output_tokens[0], skip_special_tokens=True)

def extract_json(generated_text):
    try:
        if "[MODEL]:" in generated_text:
            json_part = generated_text.split("[MODEL]:")[-1]
        else:
            json_part = generated_text

        start_idx = json_part.find('{')
        end_idx = json_part.rfind('}')
        
        if start_idx == -1 or end_idx == -1:
            return None
            
        clean_json = json_part[start_idx:end_idx+1]
        return json.loads(clean_json)
    except Exception as e:
        print(f"Parsing error: {e}")
        return None
    
def save_output(data, prompt, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filename = re.sub(r'[^\w\s-]', '', prompt).strip().lower().replace(' ', '_')
    output_path = os.path.join(output_dir, f"{filename}.json")
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✔ Saved to: {output_path}")

def main():
    MODEL_PATH = "./inference/minecraft-model-forge-finetuned"
    OUTPUT_DIR = "inference/outputs/"
    
    print("Loading model... this may take a moment.")
    model, tokenizer = load_model(MODEL_PATH)
    print("Model Loaded! Ready for Minecraft prompts.")
    
    while True:
        prompt = input("\nEnter a Minecraft block name (or 'quit'): ")
        if prompt.lower() == 'quit':
            break
            
        print("Generating...")
        generated = generate(prompt, model, tokenizer)
        data = extract_json(generated)
        
        if data is None:
            print("❌ Failed to generate valid JSON. The model might have hallucinated. Try again!")
        else:
            save_output(data, prompt, OUTPUT_DIR)

if __name__ == "__main__":
    main()