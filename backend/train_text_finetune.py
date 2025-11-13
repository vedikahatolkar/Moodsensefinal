# Template: Fine-tune a HuggingFace transformer on GoEmotions
# Usage: python train_text_finetune.py --output_dir=./checkpoints --epochs 3
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model_name', default='distilbert-base-uncased')
parser.add_argument('--output_dir', default='./checkpoints')
parser.add_argument('--epochs', type=int, default=3)
args = parser.parse_args()

print('Loading GoEmotions...')
ds = load_dataset('go_emotions')
tokenizer = AutoTokenizer.from_pretrained(args.model_name)
def tokenize(batch):
    return tokenizer(batch['text'], truncation=True, padding='max_length', max_length=128)
ds = ds.map(tokenize, batched=True)
num_labels = max(max(ds['train']['labels']))+1
model = AutoModelForSequenceClassification.from_pretrained(args.model_name, num_labels=num_labels)

training_args = TrainingArguments(output_dir=args.output_dir, num_train_epochs=args.epochs, per_device_train_batch_size=16, evaluation_strategy='epoch')
trainer = Trainer(model=model, args=training_args, train_dataset=ds['train'], eval_dataset=ds['validation'])
trainer.train()
trainer.save_model(args.output_dir)
print('Done.')
