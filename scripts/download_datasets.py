# Scripts to fetch datasets for fine-tuning.
# GOEMOTIONS:
#   uses Hugging Face datasets
#   python -c "from datasets import load_dataset; ds=load_dataset('go_emotions')"
#
# RAVDESS:
#   RAVDESS is available via Zenodo or other mirrors. There is no single hf dataset id.
#   You can download RAVDESS .zip from:
#   https://zenodo.org/record/1188976 (example link; verify)
#
# Example: download GoEmotions:
from datasets import load_dataset
ds = load_dataset('go_emotions')
print('GoEmotions loaded. Examples:', ds['train'][0])
print('For RAVDESS, download archive manually from zenodo or Kaggle and extract to data/ravdess')
