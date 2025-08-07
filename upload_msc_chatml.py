#!/usr/bin/env python3
"""
Direct upload of MSC ChatML data to Hugging Face.
"""

import json
import logging
from pathlib import Path
from datasets import Dataset, DatasetDict
from tqdm import tqdm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_msc_chatml_data(file_path: str) -> list:
    """Load MSC ChatML data from JSONL file."""
    print(f"📂 Loading data from {file_path}")
    
    conversations = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in tqdm(f, desc="Loading conversations"):
            line = line.strip()
            if line:
                data = json.loads(line)
                conversations.append(data)
    
    print(f"✅ Loaded {len(conversations)} conversations")
    return conversations

def create_dataset(conversations: list) -> Dataset:
    """Create Hugging Face dataset from conversations."""
    print("🔧 Creating dataset...")
    
    dataset_data = []
    for conv in conversations:
        messages = conv.get('messages', [])
        if messages:
            dataset_data.append({'messages': messages})
    
    dataset = Dataset.from_list(dataset_data)
    print(f"✅ Created dataset with {len(dataset)} conversations")
    return dataset

def split_dataset(dataset: Dataset) -> DatasetDict:
    """Split dataset into train/validation/test sets."""
    print("✂️ Splitting dataset...")
    
    total_size = len(dataset)
    train_size = int(total_size * 0.8)
    val_size = int(total_size * 0.1)
    
    train_dataset = dataset.select(range(train_size))
    val_dataset = dataset.select(range(train_size, train_size + val_size))
    test_dataset = dataset.select(range(train_size + val_size, total_size))
    
    dataset_dict = DatasetDict({
        'train': train_dataset,
        'validation': val_dataset,
        'test': test_dataset
    })
    
    print(f"✅ Split: train={len(train_dataset)}, validation={len(val_dataset)}, test={len(test_dataset)}")
    return dataset_dict

def upload_to_huggingface(dataset_dict: DatasetDict, repo_name: str = "msc_chatml") -> None:
    """Upload dataset to Hugging Face."""
    repo_id = f"Alexjiuqiaoyu/{repo_name}"
    
    print(f"🚀 Uploading to {repo_id}...")
    
    dataset_dict.push_to_hub(
        repo_id,
        private=False,
        commit_message="Add MSC ChatML dataset"
    )
    
    print(f"✅ Successfully uploaded to https://huggingface.co/datasets/{repo_id}")

def main():
    """Main function."""
    print("🚀 MSC ChatML Upload to Hugging Face")
    print("=" * 50)
    
    # File path
    input_file = "data/processed/msc_chatml.jsonl"
    
    # Check if file exists
    if not Path(input_file).exists():
        print(f"❌ File not found: {input_file}")
        return
    
    # Load data
    conversations = load_msc_chatml_data(input_file)
    
    if not conversations:
        print("❌ No conversations loaded!")
        return
    
    # Create dataset
    dataset = create_dataset(conversations)
    
    # Split dataset
    dataset_dict = split_dataset(dataset)
    
    # Upload to Hugging Face
    upload_to_huggingface(dataset_dict)
    
    print("\n🎉 Upload completed!")

if __name__ == "__main__":
    main() 