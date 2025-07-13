import os
from typing import Dict, Any, Optional
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import json

class LLMRouter:
    def __init__(self, use_cline: bool = True):
        load_dotenv()
        self.use_cline = use_cline
        if not self.use_cline:
            self.client = OpenAI(
                api_key=os.getenv('OPENROUTER_API_KEY'),
                base_url=os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
            )
        else:
            self.client = None
        self.models = {
            'gpt-4': {'cost_per_token': 0.03, 'capabilities': 5.0, 'max_tokens': 8192},
            'gpt-3.5-turbo': {'cost_per_token': 0.002, 'capabilities': 3.0, 'max_tokens': 4096},
            'claude-3-sonnet-20240229': {'cost_per_token': 0.01, 'capabilities': 4.5, 'max_tokens': 100000},
            'claude-3-opus-20240229': {'cost_per_token': 0.001, 'capabilities': 3.5, 'max_tokens': 100000}
        }
        self.shared_memory = {}
        self.current_model = None

    def calculate_cost(self, model_name: str, tokens: int) -> float:
        """Calculate cost for a given model and token count."""
        return self.models[model_name]['cost_per_token'] * tokens

    def select_model(self, prompt: str, max_tokens: int = 1000, budget: float = None) -> str:
        """Select the most appropriate model based on prompt requirements and budget."""
        prompt_tokens = len(prompt.split())
        total_tokens = prompt_tokens + max_tokens

        # Filter models based on token limit
        valid_models = {
            name: info for name, info in self.models.items()
            if total_tokens <= info['max_tokens']
        }

        if not valid_models:
            raise ValueError("No model available that can handle the required token count")

        if budget is None:
            # If no budget specified, choose model with highest capabilities
            best_model = max(valid_models.items(), key=lambda x: x[1]['capabilities'])[0]
        else:
            # Calculate cost for each model and select the most capable within budget
            model_costs = {
                name: self.calculate_cost(name, total_tokens)
                for name in valid_models
            }
            
            affordable_models = {
                name: valid_models[name] for name, cost in model_costs.items()
                if cost <= budget
            }
            
            if not affordable_models:
                raise ValueError(f"No model available within the specified budget of ${budget}")
            
            best_model = max(affordable_models.items(), key=lambda x: x[1]['capabilities'])[0]

        self.current_model = best_model
        return best_model

    def ask_cline(self, prompt: str) -> str:
        """Send a prompt to cline-cli and return the response."""
        result = subprocess.run([
            "cline-cli", "task", prompt
        ], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Cline CLI error: {result.stderr}")
        return result.stdout.strip()

    def chat(self, messages: list, max_tokens: int = 1000, budget: float = None):
        """Send a chat request via Cline or OpenRouter depending on configuration."""
        # If using Cline, forward the entire conversation as one prompt
        if self.use_cline:
            prompt = "\n".join([msg.get("content", "") for msg in messages])
            if self.shared_memory:
                prompt = f"Previous conversation context: {json.dumps(self.shared_memory)}\n" + prompt
            return self.ask_cline(prompt)

        # ----- OpenRouter path (original behaviour) -----
        model = self.select_model(messages[-1]['content'], max_tokens, budget)

        if self.shared_memory and (
            not messages or not isinstance(messages[0], dict) or "Previous conversation context:" not in messages[0].get("content", "")
        ):
            context = [{"role": "system", "content": "Previous conversation context:" + json.dumps(self.shared_memory)}]
            messages = context + messages
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error with {model}: {str(e)}")
            remaining_models = [m for m in self.models if m != model]
            if remaining_models:
                fallback_model = remaining_models[0]
                print(f"Falling back to {fallback_model}")
                return self.chat(messages, max_tokens, budget)
            else:
                raise


    def update_shared_memory(self, key: str, value: Any) -> None:
        """Update shared memory with new information."""
        self.shared_memory[key] = value

    def get_shared_memory(self, key: str) -> Optional[Any]:
        """Retrieve value from shared memory."""
        return self.shared_memory.get(key)

# Example usage
def main():
    router = LLMRouter()
    
    # Example conversation
    messages = [
        {"role": "user", "content": "Explain quantum computing in simple terms."},
        {"role": "assistant", "content": ""}
    ]
    
    # Chat with budget constraint
    response = router.chat(messages, max_tokens=2000, budget=0.1)
    print(f"Response: {response}")
    
    # Update shared memory
    router.update_shared_memory('last_topic', 'quantum computing')
    
    # Retrieve from shared memory
    print(f"Last topic discussed: {router.get_shared_memory('last_topic')}")

if __name__ == "__main__":
    main()
