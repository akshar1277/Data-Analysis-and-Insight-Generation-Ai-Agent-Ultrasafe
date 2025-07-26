from crewai import Agent
import pandas as pd
from scipy.stats import shapiro, levene

class StatisticalAnalysisAgent(Agent):
    def analyze(self, data, exploration_summary):
        """
        Analyze the dataset, calculate problem frequencies, and check statistical assumptions.
        """
        results = {}
        problem_counts = data['PROBLEM'].value_counts()
        total = len(data)
        problem_percentages = (problem_counts / total * 100).round(2).to_dict()
        top_issues = dict(list(problem_percentages.items())[:5])
        results['top_issues_percentages'] = top_issues
        results['all_issue_percentages'] = problem_percentages
        numeric_cols = data.select_dtypes(include='number').columns
        assumption_checks = {}
        suggestions = []
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            col_data = data[col].dropna()

          
            if len(col_data) > 5000:
                col_data = col_data.sample(n=5000, random_state=42)

            stat, p = shapiro(col_data)
            assumption_checks['normality'] = p > 0.05

            if p <= 0.05:
                suggestions.append(
                    'Normality assumption violated for t-test. Consider non-parametric alternatives (e.g., Mann-Whitney U test).'
            )
            if 'PROBLEM' in data.columns and data['PROBLEM'].nunique() > 1:
                groups = [g[1][col].dropna() for g in data.groupby('PROBLEM') if len(g[1][col].dropna()) > 1]
                if len(groups) > 1:
                    stat, p = levene(*groups)
                    assumption_checks['homoscedasticity'] = p > 0.05
                    if p <= 0.05:
                        suggestions.append('Equal variance assumption violated for ANOVA/t-test. Consider Welch’s test or non-parametric alternatives.')
        results['assumption_checks'] = assumption_checks
        results['suggestions'] = suggestions
        return results 