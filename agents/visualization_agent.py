from crewai import Agent
import matplotlib.pyplot as plt
import pandas as pd
import os
import openai
import json
import yaml
import numpy as np
from ultrasafe_client.ultrasafe import UltraSafe
class VisualizationAgent(Agent):
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

    def _reduce_context(self, summary):
        return {
            'columns': summary['columns'][:5],
            'dtypes': {k: v for k, v in list(summary['dtypes'].items())[:5]},
            'sample_values': {k: v for k, v in list(summary['sample_values'].items())[:5]},
            'exploration_summary': {
                'most_common_problems': dict(list(summary.get('exploration_summary', {}).get('most_common_problems', {}).items())[:3]),
                'unique_problem_count': summary.get('exploration_summary', {}).get('unique_problem_count', 0),
                'rare_problems': summary.get('exploration_summary', {}).get('rare_problems', [])[:3],
                'quality_issues': summary.get('exploration_summary', {}).get('quality_issues', [])[:2]
            },
            'analysis_results': {
                'top_issues_percentages': dict(list(summary.get('analysis_results', {}).get('top_issues_percentages', {}).items())[:3]),
                'assumption_checks': summary.get('analysis_results', {}).get('assumption_checks', {}),
                'suggestions': summary.get('analysis_results', {}).get('suggestions', [])[:2]
            }
        }

    def _plot_top_problems(self, data, output_dir, N=5):
        counts = data['PROBLEM'].value_counts(normalize=True) * 100
        top_counts = counts.head(N)
        plt.figure(figsize=(12,6))
        plt.bar(top_counts.index, top_counts.values, color='skyblue')
        plt.ylabel('Percentage of Occurrences')
        plt.xlabel('Problem')
        plt.title(f'Top {N} Most Common Problems')
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        fpath = os.path.join(output_dir, f'top_{N}_problems.png')
        plt.savefig(fpath)
        plt.close()
        print(f"[VisualizationAgent] Top {N} problems plot saved: {fpath}")
        return fpath

    def visualize(self, data, analysis_results, exploration_summary=None):
        output_dir = 'visualizations'
        os.makedirs(output_dir, exist_ok=True)
        file_paths = []
        # Always generate the top 5 problems plot
        top_problems_path = self._plot_top_problems(data, output_dir, N=5)
        file_paths.append(top_problems_path)
        summary = {
            'columns': [col for col in data.columns if col != 'IDENT'],
            'dtypes': {col: str(dtype) for col, dtype in data.dtypes.items() if col != 'IDENT'},
            'sample_values': {col: vals for col, vals in data.head(3).to_dict().items() if col != 'IDENT'},
            'exploration_summary': exploration_summary,
            'analysis_results': analysis_results
        }
        reduced = self._reduce_context(summary)
        serializable = self._to_json(reduced)
        prompt_path = os.path.join(self._prompt_dir, 'llm_viz_prompt.yaml')
        try:
            with open(prompt_path, 'r') as f:
                prompt_template = yaml.safe_load(f)['prompt']
        except Exception as e:
            print(f"Prompt YAML error: {e}")
            return file_paths
        prompt = prompt_template.format(dataset_summary=json.dumps(serializable, indent=2))
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
                max_tokens=1200
            )
            llm_content = llm_content = response["choices"][0]["message"]["content"]  

            try:
                plot_instructions = json.loads(llm_content)
            except Exception:
                import re
                match = re.search(r'\[.*\]', llm_content, re.DOTALL)
                if match:
                    plot_instructions = json.loads(match.group(0))
                else:
                    print("Could not parse LLM output as JSON.")
                    return file_paths
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return file_paths
        for idx, instr in enumerate(plot_instructions):
            plot_type = instr.get('plot_type')
            columns = instr.get('columns', [])
            # Skip any plot that uses IDENT as a column
            if 'IDENT' in columns:
                print(f"[VisualizationAgent] Skipping plot {plot_type} with IDENT column.")
                continue
            desc = instr.get('description', f'plot_{idx}')
            fname = f"{plot_type}_{'_'.join(columns)}_{idx}.png".replace(' ', '_')
            fpath = os.path.join(output_dir, fname)
            try:
                N = 10
                if plot_type == 'bar' and len(columns) == 1:
                    counts = data[columns[0]].value_counts()
                    top_counts = counts[:N]
                    other_count = counts[N:].sum()
                    labels = list(top_counts.index) + (["Other"] if other_count > 0 else [])
                    values = list(top_counts.values) + ([other_count] if other_count > 0 else [])
                    plt.figure(figsize=(10,6))
                    plt.bar(labels, values)
                    plt.xlabel(columns[0])
                    plt.ylabel('Count')
                    plt.title(desc)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    plt.savefig(fpath)
                    plt.close()
                    print(f"[VisualizationAgent] Bar plot saved: {fpath}")
                elif plot_type == 'pie' and len(columns) == 1:
                    counts = data[columns[0]].value_counts()
                    top_counts = counts[:N]
                    other_count = counts[N:].sum()
                    labels = list(top_counts.index) + (["Other"] if other_count > 0 else [])
                    values = list(top_counts.values) + ([other_count] if other_count > 0 else [])
                    plt.figure(figsize=(8,8))
                    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
                    plt.title(desc)
                    plt.savefig(fpath)
                    plt.close()
                    print(f"[VisualizationAgent] Pie chart saved: {fpath}")
                elif plot_type == 'histogram' and len(columns) == 1:
                    if pd.api.types.is_numeric_dtype(data[columns[0]]):
                        plt.figure(figsize=(8,6))
                        plt.hist(data[columns[0]].dropna(), bins=20, color='lightgreen', edgecolor='black')
                        plt.xlabel(columns[0])
                        plt.ylabel('Frequency')
                        plt.title(desc)
                        plt.tight_layout()
                        plt.savefig(fpath)
                        plt.close()
                        print(f"[VisualizationAgent] Histogram saved: {fpath}")
                    else:
                        counts = data[columns[0]].value_counts()
                        top_counts = counts[:N]
                        other_count = counts[N:].sum()
                        labels = list(top_counts.index) + (["Other"] if other_count > 0 else [])
                        values = list(top_counts.values) + ([other_count] if other_count > 0 else [])
                        plt.figure(figsize=(10,6))
                        plt.bar(labels, values)
                        plt.xlabel(columns[0])
                        plt.ylabel('Count')
                        plt.title(desc + " (Top 10)")
                        plt.xticks(rotation=45, ha='right')
                        plt.tight_layout()
                        plt.savefig(fpath)
                        plt.close()
                        print(f"[VisualizationAgent] Histogram (categorical as bar) saved: {fpath}")
                elif plot_type == 'boxplot' and len(columns) == 1:
                    if pd.api.types.is_numeric_dtype(data[columns[0]]):
                        plt.figure(figsize=(6,6))
                        plt.boxplot(data[columns[0]].dropna())
                        plt.ylabel(columns[0])
                        plt.title(desc)
                        plt.tight_layout()
                        plt.savefig(fpath)
                        plt.close()
                        print(f"[VisualizationAgent] Boxplot saved: {fpath}")
                    else:
                        counts = data[columns[0]].value_counts()
                        top_counts = counts[:N]
                        other_count = counts[N:].sum()
                        labels = list(top_counts.index) + (["Other"] if other_count > 0 else [])
                        values = list(top_counts.values) + ([other_count] if other_count > 0 else [])
                        plt.figure(figsize=(10,6))
                        plt.bar(labels, values)
                        plt.xlabel(columns[0])
                        plt.ylabel('Count')
                        plt.title(desc + " (Top 10)")
                        plt.xticks(rotation=45, ha='right')
                        plt.tight_layout()
                        plt.savefig(fpath)
                        plt.close()
                        print(f"[VisualizationAgent] Boxplot (categorical as bar) saved: {fpath}")
                elif plot_type == 'scatter' and len(columns) == 2:
                    x, y = columns[0], columns[1]
                    if 'IDENT' in [x, y]:
                        print(f"[VisualizationAgent] Skipping scatter plot with IDENT column.")
                        continue
                    if pd.api.types.is_numeric_dtype(data[x]) and pd.api.types.is_numeric_dtype(data[y]):
                        plt.figure(figsize=(8,6))
                        plt.scatter(data[x], data[y], alpha=0.5)
                        plt.xlabel(x)
                        plt.ylabel(y)
                        plt.title(desc)
                        plt.tight_layout()
                        plt.savefig(fpath)
                        plt.close()
                        print(f"[VisualizationAgent] Scatter plot saved: {fpath}")
                    else:
                        x_counts = data[x].value_counts()[:N].index
                        y_counts = data[y].value_counts()[:N].index
                        filtered = data[data[x].isin(x_counts) & data[y].isin(y_counts)]
                        plt.figure(figsize=(10,6))
                        plt.scatter(filtered[x], filtered[y], alpha=0.5)
                        plt.xlabel(x)
                        plt.ylabel(y)
                        plt.title(desc + " (Top 10)")
                        plt.tight_layout()
                        plt.savefig(fpath)
                        plt.close()
                        print(f"[VisualizationAgent] Scatter plot (categorical filtered) saved: {fpath}")
                elif plot_type == 'heatmap' and columns == ['missing']:
                    import seaborn as sns
                    plt.figure(figsize=(10,6))
                    sns.heatmap(data.isnull(), cbar=False)
                    plt.title(desc)
                    plt.tight_layout()
                    plt.savefig(fpath)
                    plt.close()
                    print(f"[VisualizationAgent] Heatmap saved: {fpath}")
                else:
                    print(f"[VisualizationAgent] Plot type '{plot_type}' with columns {columns} not supported. Skipping.")
                    continue
                file_paths.append(fpath)
            except Exception as e:
                print(f"[VisualizationAgent] Error generating plot {desc}: {e}")
                continue
        print(f"[VisualizationAgent] Final list of generated visualizations: {file_paths}")
        return file_paths 