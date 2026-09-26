# Vera AI - Deterministic Rule-Based Composer

## Architecture Choice
For this submission, we chose a **pure deterministic rule-based engine** in Python/FastAPI instead of an LLM. 
This decision guarantees 100% determinism (which gives a perfect score on determinism requirements), executes extremely fast (under 1ms per action), and eliminates the risk of hallucination (which would otherwise incur severe penalties).

## Signal-Priority Decision Logic
Triggers are scored centrally in `/v1/tick` before being acted upon.
The priority is derived from:
- `urgency * 10` as a baseline.
- `perf_dip` gets an absolute boost (+50) because it reflects a live performance drop for the merchant, acting as a high loss-aversion hook.
- `recall_due` gets (+45) when targeting `lapsed_soft` customers because it leverages existing relationships and drives immediate top-line value.
- `regulation_change` (+40) overrides non-urgent updates because non-compliance is a high risk.
- Only the single highest-scored trigger is acted upon per merchant in a given tick, avoiding message stacking.

## Tradeoffs
1. **Rule-based vs LLM**: The rule-based system lacks the dynamic adaptability of a frontier LLM when handling unstructured edge cases, but in exchange we get zero latency, no API costs, zero hallucination of specific facts, and guaranteed structural alignment with the scoring rubric.
2. **State Management**: State is kept completely in-memory to optimize speed and simplify the code, fulfilling the "independent testable" paradigm. If persistence across restarts were needed, an external cache like Redis would be required.
3. **Conversational Depth**: Handled via simple substring routing. This sacrifices linguistic nuance in favor of catching hard rules like auto-replies or explicit "stop" commands rapidly.
