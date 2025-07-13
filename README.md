# OpenRouter LLM Switcher

This project implements an intelligent LLM router that optimizes between different language models based on cost and capabilities while maintaining shared memory for context persistence.

## Features

- Automatic model selection based on:
  - Token requirements
  - Budget constraints
  - Model capabilities
- Shared memory system for context persistence
- Fallback mechanism for failed requests
- Support for multiple OpenRouter models
- Cost-aware optimization

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Usage

```python
from llm_switcher import LLMRouter

router = LLMRouter()

# Chat with budget constraint
messages = [
    {"role": "user", "content": "Your prompt here"},
    {"role": "assistant", "content": ""}
]

response = router.chat(messages, max_tokens=2000, budget=0.1)

# Update shared memory
router.update_shared_memory('key', 'value')

# Retrieve from shared memory
value = router.get_shared_memory('key')
```

## Model Selection Criteria

The router automatically selects the most appropriate model based on:
- Token requirements
- Budget constraints (if specified)
- Model capabilities (higher capabilities preferred within budget)
- Token limits of each model

## Supported Models

- GPT-4
- GPT-3.5-Turbo
- Claude-3 Sonnet
- Claude-3 Opus

## Error Handling

- Automatic fallback to alternative models if the primary choice fails
- Clear error messages for budget and token limit issues
- Graceful handling of API errors
