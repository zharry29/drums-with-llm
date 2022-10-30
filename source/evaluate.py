import json
import openai
from text_to_midi import convert_to_midi
import sys

openai.api_key_path = "../source/api_keys/harry.key"
model = sys.argv[1]
model_to_name = {
    "davinci": "davinci:ft-ccb-lab-members-2022-10-30-05-55-23",
    "curie": "curie:ft-ccb-lab-members-2022-10-28-02-14-43",
    "ada": "ada:ft-ccb-lab-members-2022-10-30-15-30-17"
}

def prompt_gpt3(prompt):
    res = openai.Completion.create(
        model=model_to_name[model],
        prompt=prompt,
        temperature=0.9,
        max_tokens=1000,
        stop=['END']
    )
    return res["choices"][0]["text"]

for split in ["dev", "test"]:
    with open(f"../gpt3_{split}.jsonl") as f:
        for line in f:
            d = json.loads(line)
            prompt = d["prompt"]
            name = d["name"]
            gen = prompt_gpt3(prompt)
            gen_score = prompt + gen
            gen_score = gen_score.replace('SEP\n','')
            #print(prompt)
            #print('========')
            #print(gen)
            with open(f"../output_text_{model}/{split}/{name}.txt", 'w') as fw:
                fw.write(gen_score)
            try:
                convert_to_midi(gen_score, f"../output_midi_{model}/{split}/{name}.mid")
            except:
                print(name)
                print("Error")
                continue
            #break
        #break