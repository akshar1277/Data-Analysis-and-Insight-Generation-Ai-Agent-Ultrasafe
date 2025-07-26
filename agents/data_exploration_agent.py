from crewai import Agent

class DataExplorationAgent(Agent):
    def analyze(self, data):
        """
        Explore the dataset to find common patterns, rare problems, and data quality issues.
        """
        problem_counts = data['PROBLEM'].value_counts()
        most_common = problem_counts.head(5).to_dict()
        unique_problems = data['PROBLEM'].nunique()
        quality_issues = []
        if data['PROBLEM'].isnull().any():
            quality_issues.append('Missing PROBLEM entries')
        if data['ACTION'].isnull().any():
            quality_issues.append('Missing ACTION entries')
        rare_problems = problem_counts[problem_counts == 1].index.tolist()
        return {
            "most_common_problems": most_common,
            "unique_problem_count": unique_problems,
            "rare_problems": rare_problems,
            "quality_issues": quality_issues
        } 