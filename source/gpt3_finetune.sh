export OPENAI_API_KEY="sk-iXLNzsfdPX99vPiEDZxST3c5dcoxHcUKQbRVq4pg"
openai api fine_tunes.create -t ../gpt3_train.jsonl -m curie
openai api completions.create -m curie:ft-ccb-lab-members-2022-01-11-05-33-17 -p ""
