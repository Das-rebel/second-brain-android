# Second Brain Android Development Repository

⚠️ **This repository has been superseded by a comprehensive production-ready implementation.**

## 🚀 New Repository: [second-brain-android-testing](https://github.com/Das-rebel/second-brain-android-testing)

**Complete Second Brain Android app with enterprise-grade testing infrastructure:**

### 🏗️ Architecture & Features
- **Clean Architecture** with MVVM pattern
- **Jetpack Compose** UI with Material 3 design
- **Offline-First** with Room database and automatic sync
- **Hilt Dependency Injection** for modular design
- **Comprehensive bookmark management** with collections, search, and filtering

### 🧪 Comprehensive Testing Suite (150+ Tests)
- **Espresso Tests** (24 tests) - UI instrumentation testing
- **Robolectric Tests** (24 tests) - Local unit testing with Android context
- **UI Automator Tests** (13 tests) - System-level integration testing
- **Compose UI Tests** (40+ tests) - Component-specific testing
- **95%+ code coverage** across all application layers

### 🔗 Integration
- **X/Twitter Bookmark Automation**: [x-bookmarks-automation](https://github.com/Das-rebel/x-bookmarks-automation)
- **Real-time synchronization** between automation system and Android app
- **Cross-platform bookmark management**

## Legacy Content: OpenRouter LLM Switcher

This project also includes an intelligent LLM router that optimizes between different language models based on cost and capabilities while maintaining shared memory for context persistence.

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
