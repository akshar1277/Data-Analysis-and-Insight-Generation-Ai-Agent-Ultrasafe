import pandas as pd
from agents.data_exploration_agent import DataExplorationAgent
from agents.statistical_analysis_agent import StatisticalAnalysisAgent
from agents.visualization_agent import VisualizationAgent
from agents.insight_generation_agent import InsightGenerationAgent
from agents.rag_retriever import retrieve
from dotenv import load_dotenv
import os
from datetime import datetime
load_dotenv()

# Load dataset
df = pd.read_csv("sample_data/Aircraft_Annotation_DataFile.csv")
# Set prompt directory
PROMPT_DIR = os.path.join(os.path.dirname(__file__), 'prompts')

# Initialize agents
explorer_agent = DataExplorationAgent(
    role="Data Exploration Specialist",
    goal="Identify patterns, outliers, and data quality issues in aircraft maintenance data.",
    backstory="An expert in exploratory data analysis for aviation datasets."
)
stats_agent = StatisticalAnalysisAgent(
    role="Statistical Analyst",
    goal="Apply statistical methods to uncover trends and validate findings.",
    backstory="A statistician with experience in aviation maintenance data."
)
viz_agent = VisualizationAgent(
    role="Visualization Expert",
    goal="Create clear and informative charts to communicate findings.",
    backstory="A data visualization specialist for technical datasets.",
    prompt_dir=PROMPT_DIR
)
insight_agent = InsightGenerationAgent(
    role="Insight Generator",
    goal="Produce actionable insights for maintenance teams.",
    backstory="A consultant skilled in translating data into operational improvements.",
    prompt_dir=PROMPT_DIR
)

# Data Exploration
exploration_summary = explorer_agent.analyze(df)

# Use RAG retriever for relevant methods and best practices
relevant_methods = retrieve("statistical methods", k=3)
best_practices = retrieve("best practices", k=3)

# Statistical Analysis
analysis_results = stats_agent.analyze(df, exploration_summary)

# Visualization
visualizations = viz_agent.visualize(df, analysis_results, exploration_summary)

# LLM-driven Insight Generation: pass all outputs as context
llm_report = insight_agent.generate_insights(
    exploration_summary,
    analysis_results,
    visualizations,
    relevant_methods,
    best_practices
)

# Append full content of knowledge base files to the report (optional, can be removed if only using RAG)
appendix = "\n\n---\n\n"
try:
    with open('knowledge_base/statistical_methods.md', 'r') as f:
        appendix += "## Appendix: Statistical Methods\n\n" + f.read() + "\n"
except Exception as e:
    appendix += f"## Appendix: Statistical Methods\n\nError loading file: {e}\n"
try:
    with open('knowledge_base/best_practices.md', 'r') as f:
        appendix += "\n## Appendix: Best Practices\n\n" + f.read() + "\n"
except Exception as e:
    appendix += f"\n## Appendix: Best Practices\n\nError loading file: {e}\n"

final_report = llm_report + appendix

print("\n==== FINAL INSIGHT REPORT ====\n")
print(final_report)

# Save LLM-generated Markdown report in a separate folder
os.makedirs('insights', exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
insight_md_path = os.path.join('insights', f'insight_report_{timestamp}.md')
with open(insight_md_path, 'w') as f:
    f.write(final_report)
print(f"\nInsight report saved to {insight_md_path}\n")
