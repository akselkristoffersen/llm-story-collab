from huggingface_hub import snapshot_download
import os

model_name = os.environ["AX_MODEL_NAME"]
os.environ["HF_HOME"]

snapshot_download(repo_id=model_name)