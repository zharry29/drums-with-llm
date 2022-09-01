import os

for drummer_id in range(1,11):
    for session_id in range(1,4):
        try:
            for fname in os.listdir(f"../groove/drummer{drummer_id}/session{session_id}"):
                if fname.endswith('.mid') and "_beat_" in fname:
                    os.system(f"cp ../groove/drummer{drummer_id}/session{session_id}/{fname} ../data_midi/{drummer_id}_{fname}")
        except FileNotFoundError:
            continue