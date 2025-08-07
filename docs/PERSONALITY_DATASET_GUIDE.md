# Personality Dataset Creation Guide

## 🎯 **Overview**

This guide explains how to create a personality dataset where:
- **Input**: Multi-turn conversations from the MSC dataset
- **Output**: 1000-dimensional sparse vectors representing personality traits
- **Analysis**: GPT-4o analyzes conversations against 959 personality traits from `mindcode.xlsx`

## 📊 **Dataset Structure**

### Input: Multi-turn Conversations
```
Persona: I like to remodel homes.
Persona: I like to go hunting.
Persona: I like to shoot a bow.
Persona: My favorite holiday is halloween.

Message: Hi, how are you doing? I'm getting ready to do some cheetah chasing to stay in shape.
Response: You must be very fast. Hunting is one of my favorite hobbies.
Message: I am! For my hobby I like to do canning or some whittling.
Response: I also remodel homes when I am not out bow hunting.
```

### Output: 1000-Dimensional Sparse Vector
```json
{
  "id": "session_1_train_0",
  "conversation": "...",
  "personality_scores": [2, 1, 0, 5, 8, 3, 0, ...],  // 959 scores (0-10)
  "sparse_vector": [2, 1, 0, 5, 8, 3, 0, ..., 0, 0, 0],  // 1000 dimensions
  "metadata": {
    "num_traits": 959,
    "vector_dimension": 1000,
    "analysis_timestamp": 1234567890
  }
}
```

## 🛠 **Setup Instructions**

### 1. Prerequisites
- ✅ Conda environment `impersonality` with Python 3.11
- ✅ MSC dataset downloaded (`data/parlai_msc/`)
- ✅ `mindcode.xlsx` file with 959 personality traits
- ✅ OpenAI API key with GPT-4o access

### 2. Install Dependencies
```bash
conda activate impersonality
pip install openai tqdm pyyaml openpyxl
```

### 3. Verify Setup
```bash
python run_dataset_creation.py --api-key YOUR_API_KEY --sample
```

## 🚀 **Usage**

### Create Sample Dataset (5 conversations)
```bash
python run_dataset_creation.py --api-key YOUR_API_KEY --sample
```

### Create Full Dataset (100 conversations)
```bash
python run_dataset_creation.py --api-key YOUR_API_KEY --max-conversations 100
```

### Custom Configuration
```bash
python run_dataset_creation.py \
  --api-key YOUR_API_KEY \
  --max-conversations 50 \
  --output data/personality_dataset/my_dataset.jsonl \
  --delay 2.0
```

## 📋 **Command Line Options**

| Option | Description | Default |
|--------|-------------|---------|
| `--api-key` | OpenAI API key (required) | - |
| `--sample` | Create sample dataset (5 conversations) | False |
| `--max-conversations` | Maximum conversations to process | 100 |
| `--output` | Output file path | `data/personality_dataset/personality_dataset.jsonl` |
| `--delay` | Delay between API calls (seconds) | 1.0 |

## 🔍 **Personality Analysis Process**

### 1. Trait Loading
- Loads 959 personality traits from `mindcode.xlsx`
- Each trait has: ID, Chinese name, English name, Chinese description, English description

### 2. Conversation Formatting
- Converts raw MSC conversation lines to readable format
- Preserves persona information and conversation flow
- Removes silence markers and empty lines

### 3. GPT-4o Analysis
- Creates detailed prompt with all 959 traits
- Analyzes conversation for personality indicators
- Returns scores from 0-10 for each trait
- Uses low temperature (0.1) for consistency

### 4. Vector Creation
- Converts 959 scores to 1000-dimensional sparse vector
- Pads with zeros to reach 1000 dimensions
- Preserves original scores for reference

## 📁 **Output Files**

### Main Dataset
- **Format**: JSON Lines (`.jsonl`)
- **Location**: `data/personality_dataset/personality_dataset.jsonl`
- **Structure**: One JSON object per line

### Logs
- **File**: `personality_dataset_creation.log`
- **Content**: Processing progress, errors, warnings

### Sample Entry
```json
{
  "id": "session_1_train_0",
  "session": 1,
  "split": "train",
  "conversation": "Persona: I like to remodel homes...",
  "personality_scores": [2, 1, 0, 5, 8, 3, 0, ...],
  "sparse_vector": [2, 1, 0, 5, 8, 3, 0, ..., 0, 0, 0],
  "metadata": {
    "num_traits": 959,
    "vector_dimension": 1000,
    "analysis_timestamp": 1234567890
  }
}
```

## 💰 **Cost Estimation**

### GPT-4o API Costs
- **Input tokens**: ~2000-4000 per conversation
- **Output tokens**: ~2000 per analysis
- **Total tokens**: ~4000-6000 per conversation
- **Cost per conversation**: ~$0.02-0.03
- **Cost for 100 conversations**: ~$2-3

### Optimization Tips
- Use `--delay` to control API call rate
- Start with `--sample` to test
- Monitor costs in OpenAI dashboard
- Consider batching for large datasets

## 🔧 **Advanced Configuration**

### Custom Configuration File
Edit `dataset_config.yaml` to modify:
- OpenAI model settings
- Processing parameters
- Output format options
- Quality control settings

### Custom Personality Traits
- Modify `mindcode.xlsx` to add/remove traits
- Update `num_traits` in configuration
- Adjust vector dimensions accordingly

## 📊 **Quality Control**

### Automatic Checks
- ✅ Validates score ranges (0-10)
- ✅ Ensures correct vector dimensions (1000)
- ✅ Logs processing errors
- ✅ Skips short conversations

### Manual Verification
```python
import json
import pandas as pd

# Load dataset
with open('data/personality_dataset/personality_dataset.jsonl', 'r') as f:
    entries = [json.loads(line) for line in f]

# Check statistics
print(f"Total entries: {len(entries)}")
print(f"Average vector length: {np.mean([len(e['sparse_vector']) for e in entries])}")
print(f"Average non-zero scores: {np.mean([sum(1 for x in e['personality_scores'] if x > 0) for e in entries])}")
```

## 🚨 **Troubleshooting**

### Common Issues

1. **API Key Error**
   ```
   ❌ OpenAI API key not valid
   ```
   **Solution**: Check your API key and ensure it has GPT-4o access

2. **Missing MSC Data**
   ```
   ❌ MSC data not found! Please run the dataset download first.
   ```
   **Solution**: Run the MSC dataset download script first

3. **Missing mindcode.xlsx**
   ```
   ❌ mindcode.xlsx not found!
   ```
   **Solution**: Ensure the file is in the project root directory

4. **Rate Limiting**
   ```
   ❌ Rate limit exceeded
   ```
   **Solution**: Increase `--delay` parameter (e.g., `--delay 2.0`)

### Error Logs
Check `personality_dataset_creation.log` for detailed error information.

## 📈 **Next Steps**

### Model Training
- Use the generated dataset to train personality prediction models
- Implement sparse vector classification/regression
- Evaluate model performance on held-out conversations

### Dataset Expansion
- Process more conversations from MSC dataset
- Add other conversation datasets
- Implement data augmentation techniques

### Analysis Tools
- Create visualization tools for personality vectors
- Implement trait correlation analysis
- Build conversation-to-personality mapping tools

## 🔗 **References**

- [ParlAI MSC Dataset](https://parl.ai/projects/msc/)
- [OpenAI GPT-4o API](https://platform.openai.com/docs/models/gpt-4o)
- [Personality AI Creation Guide](https://chatgpt.com/g/g-5Py8sPmwG-personality-ai-creator)
- [Fine-tuning GPT-3.5 for Personality](https://generativeai.pub/i-fine-tuned-a-human-like-persona-into-gpt-3-5-here-are-the-results-e724cc662787)

---

**Created**: August 3, 2025  
**Environment**: Python 3.11 + OpenAI GPT-4o  
**Dataset**: MSC Conversations → 1000D Personality Vectors  
**Status**: Ready for personality prediction research 