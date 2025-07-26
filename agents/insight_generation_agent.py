from crewai import Agent
import openai
import os
import yaml
import json
import numpy as np
from ultrasafe_client.ultrasafe import UltraSafe

class InsightGenerationAgent(Agent):
    def __init__(self, *args, prompt_dir=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._prompt_dir = prompt_dir or os.path.dirname(__file__)

    def _to_json(self, obj):
        if isinstance(obj, dict):
            return {k: self._to_json(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._to_json(v) for v in obj]
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        if isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        return obj

    def _summarize_kb(self, entries, max_items=3):
        summary = []
        for entry in entries[:max_items]:
            lines = entry.splitlines()
            title = lines[0] if lines else ''
            summary.append({'title': title, 'content': entry})
        return summary

    def generate_insights(self, exploration_summary, analysis_results, visualizations, relevant_methods=None, best_practices=None):
        """
        Use LLM to generate a comprehensive Markdown report from all agent outputs, with context reduction for large outputs.
        Args:
            exploration_summary (dict)
            analysis_results (dict)
            visualizations (list)
            relevant_methods (list)
            best_practices (list)
        Returns:
            str: Markdown report
        """
        context = {
            'exploration_summary': {
                'most_common_problems': dict(list(exploration_summary.get('most_common_problems', {}).items())[:5]),
                'unique_problem_count': exploration_summary.get('unique_problem_count', 0),
                'rare_problems': exploration_summary.get('rare_problems', [])[:5],
                'quality_issues': exploration_summary.get('quality_issues', [])
            },
            'analysis_results': {
                'top_issues_percentages': dict(list(analysis_results.get('top_issues_percentages', {}).items())[:5]),
                'assumption_checks': analysis_results.get('assumption_checks', {}),
                'suggestions': analysis_results.get('suggestions', [])[:3]
            },
            'visualizations': visualizations[:3],
            'relevant_methods': self._summarize_kb(relevant_methods or [], max_items=3),
            'best_practices': self._summarize_kb(best_practices or [], max_items=3)
        }
        serializable_context = self._to_json(context)
        prompt_path = os.path.join(self._prompt_dir, 'llm_insight_prompt.yaml')
        try:
            with open(prompt_path, 'r') as f:
                prompt_template = yaml.safe_load(f)['prompt']
        except Exception as e:
            print(f"Prompt YAML error: {e}")
            return "Error: Could not load prompt."
        prompt = prompt_template.format(context_json=json.dumps(serializable_context, indent=2))
        
        if not os.getenv("ULTRASAFE_API_KEY"):
            raise ValueError("ULTRASAFE_API_KEY environment variable not set.")

        try:
            response = UltraSafe.chat.Completions.create(
                model="usf1-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1800
            )
            llm_content = llm_content = response["choices"][0]["message"]["content"] 

            return llm_content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "Error: Could not generate LLM report." 