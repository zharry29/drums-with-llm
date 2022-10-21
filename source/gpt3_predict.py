import openai
from text_to_midi import convert_to_midi

def force_end_new_line(s):
    return s.strip() + '\n'

def prompt_gpt3(prompt):
    res = openai.Completion.create(
    model="davinci:ft-ccb-lab-members-2022-10-18-23-45-36",
    prompt=prompt,
    temperature=0.9,
    )
    return res["choices"][0]["text"]

def clean_result(res):
    lines = res.split('\n')
    lines = [l for l in lines if l]
    out_lines = []
    for line in lines:
        if len(line) != 6:
            line += '-'*(6-len(line))
        new_line = ""
        for i,char in enumerate(line):
            if char not in ['-', 'o', 'b']:
                new_line += '-'
            # ensure only RC can have b (bell)
            elif char == 'b' and i != 1:
                new_line += '-'
            else:
                new_line += char
        out_lines.append(new_line)
    return '\n'.join(out_lines)

prompt = "----o-\n------\n--o---\n------\n---oo-\n------\n--o---\n------\n"
output = prompt_gpt3(prompt)
#output = clean_result(output)
MAX_CALLS = 5
num_calls = 0
while (len(output.split('\n')) < 64):
    if (num_calls >= MAX_CALLS):
        break
    num_calls += 1

    if not prompt:
        prompt += force_end_new_line(output)
    else:
        prompt = force_end_new_line(prompt)
        prompt += force_end_new_line(output)
    output = force_end_new_line(output)
    output += prompt_gpt3(prompt)
    output = force_end_new_line(output)
print(output)

convert_to_midi(output, "../out.midi")