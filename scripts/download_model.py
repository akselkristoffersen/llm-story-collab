from huggingface_hub import snapshot_download
import os

model_name = os.environ["AX_MODEL_PATH"]
output_dir = f"./models/{model_name}/"

snapshot_download(repo_id=model_name, local_dir=output_dir)

print(f"Model {model_name} has been downloaded to {output_dir}")
