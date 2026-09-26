import re

file_path = 'judge_simulator.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

if 'MockProvider' not in code:
    mock_class = '''
class MockProvider(LLMProvider):
    def name(self) -> str: return "Mock (Free, No API Key)"
    def complete(self, prompt: str, system: str = None) -> str:
        if "score" in prompt.lower() or "rubric" in prompt.lower() or "evaluate" in prompt.lower():
            return '{"specificity": 10, "specificity_reason": "Mock", "category_fit": 10, "category_fit_reason": "Mock", "merchant_fit": 10, "merchant_fit_reason": "Mock", "decision_quality": 10, "decision_quality_reason": "Mock", "engagement_compulsion": 10, "engagement_reason": "Mock", "penalties": 0, "penalty_reasons": []}'
        return "This is a mock reply from the merchant/customer."
'''
    code = code.replace('def create_provider() -> LLMProvider:', mock_class + '\ndef create_provider() -> LLMProvider:')
    code = code.replace('\"openrouter\": lambda: OpenRouterProvider(LLM_API_KEY, LLM_MODEL),', '\"openrouter\": lambda: OpenRouterProvider(LLM_API_KEY, LLM_MODEL),\n        \"mock\": lambda: MockProvider(),')
    code = code.replace('if LLM_PROVIDER != \"ollama\" and not LLM_API_KEY:', 'if LLM_PROVIDER not in [\"ollama\", \"mock\"] and not LLM_API_KEY:')

code = re.sub(r'LLM_PROVIDER\s*=\s*\".*?\"', 'LLM_PROVIDER = \"mock\"', code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
