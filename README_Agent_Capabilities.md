# Agent Capabilities and Analysis Workflow

## Overview

This analysis system implements a multi-agent architecture for comprehensive data analysis using CrewAI framework. The system is designed to process aircraft maintenance data and generate actionable insights through a coordinated workflow of specialized agents.

## Agent Architecture

### 1. Data Exploration Agent (`DataExplorationAgent`)

**Role**: Data Exploration Specialist  
**Goal**: Identify patterns, outliers, and data quality issues in aircraft maintenance data  
**Backstory**: An expert in exploratory data analysis for aviation datasets

**Capabilities**:
- **Pattern Recognition**: Identifies most common problems and their frequencies
- **Quality Assessment**: Detects missing data and data quality issues
- **Rare Problem Detection**: Finds unique problems that occur only once
- **Statistical Summary**: Provides comprehensive dataset overview

**Key Methods**:
```python
def analyze(self, data):
    # Returns exploration summary with:
    # - most_common_problems: Top 5 problems with counts
    # - unique_problem_count: Total number of unique problems
    # - rare_problems: Problems occurring only once
    # - quality_issues: List of data quality problems
```

### 2. Statistical Analysis Agent (`StatisticalAnalysisAgent`)

**Role**: Statistical Analyst  
**Goal**: Apply statistical methods to uncover trends and validate findings  
**Backstory**: A statistician with experience in aviation maintenance data

**Capabilities**:
- **Problem Frequency Analysis**: Calculates percentage distributions of problems
- **Statistical Assumption Testing**: Validates normality and homogeneity of variance
- **Methodological Recommendations**: Suggests appropriate statistical tests
- **Data Validation**: Ensures statistical rigor in analysis

**Key Methods**:
```python
def analyze(self, data, exploration_summary):
    # Returns analysis results with:
    # - top_issues_percentages: Problem frequency percentages
    # - assumption_checks: Normality and variance tests
    # - suggestions: Recommended statistical approaches
```

**Statistical Tests Implemented**:
- Shapiro-Wilk test for normality
- Levene's test for homogeneity of variance
- Automatic detection of appropriate test selection

### 3. Visualization Agent (`VisualizationAgent`)

**Role**: Visualization Expert  
**Goal**: Create clear and informative charts to communicate findings  
**Backstory**: A data visualization specialist for technical datasets

**Capabilities**:
- **Automated Plot Generation**: Creates diverse visualization types
- **LLM-Driven Plot Selection**: Uses AI to determine optimal visualizations
- **Context-Aware Visualization**: Adapts plots based on data characteristics
- **Quality Control**: Ensures plots are meaningful and informative

**Supported Plot Types**:
- **Bar Charts**: For categorical data frequency analysis
- **Pie Charts**: For proportion visualization
- **Histograms**: For distribution analysis
- **Box Plots**: For outlier detection and distribution comparison
- **Scatter Plots**: For relationship analysis between variables
- **Heatmaps**: For missing data visualization

**Key Features**:
- Automatic handling of large datasets (top N categories)
- Context reduction for large datasets
- Integration with LLM for intelligent plot selection
- File management and organization

### 4. Insight Generation Agent (`InsightGenerationAgent`)

**Role**: Insight Generator  
**Goal**: Produce actionable insights for maintenance teams  
**Backstory**: A consultant skilled in translating data into operational improvements

**Capabilities**:
- **Comprehensive Report Generation**: Creates professional Markdown reports
- **Context Integration**: Combines outputs from all agents
- **Actionable Recommendations**: Translates findings into business insights
- **Knowledge Base Integration**: Incorporates statistical methods and best practices

**Key Methods**:
```python
def generate_insights(self, exploration_summary, analysis_results, 
                     visualizations, relevant_methods, best_practices):
    # Returns comprehensive Markdown report with:
    # - Executive summary
    # - Data exploration findings
    # - Statistical analysis results
    # - Visualization interpretations
    # - Actionable recommendations
```

## Analysis Workflow

### 1. Data Loading and Preparation
```python
# Load dataset
df = pd.read_csv("sample_data/Aircraft_Annotation_DataFile.csv")
```

### 2. Agent Initialization
```python
# Initialize all agents with specific roles and goals
explorer_agent = DataExplorationAgent(...)
stats_agent = StatisticalAnalysisAgent(...)
viz_agent = VisualizationAgent(...)
insight_agent = InsightGenerationAgent(...)
```

### 3. Sequential Analysis Pipeline

#### Step 1: Data Exploration
```python
exploration_summary = explorer_agent.analyze(df)
```
- Identifies data patterns and quality issues
- Provides foundation for subsequent analysis

#### Step 2: Knowledge Retrieval
```python
relevant_methods = retrieve("statistical methods", k=3)
best_practices = retrieve("best practices", k=3)
```
- Retrieves relevant statistical methods and best practices
- Ensures analysis follows established guidelines

#### Step 3: Statistical Analysis
```python
analysis_results = stats_agent.analyze(df, exploration_summary)
```
- Applies statistical tests and validation
- Generates quantitative insights

#### Step 4: Visualization Generation
```python
visualizations = viz_agent.visualize(df, analysis_results, exploration_summary)
```
- Creates diverse visual representations
- Supports findings with graphical evidence

#### Step 5: Insight Generation
```python
llm_report = insight_agent.generate_insights(
    exploration_summary,
    analysis_results,
    visualizations,
    relevant_methods,
    best_practices
)
```
- Synthesizes all findings into comprehensive report
- Provides actionable recommendations

### 4. Output Generation
- **Markdown Report**: Professional analysis report saved to `insights/` directory
- **Visualizations**: Charts and plots saved to `visualizations/` directory
- **Timestamped Files**: All outputs include timestamps for version control

## Key Features

### Context Management
- **Reduced Context**: Large datasets are summarized to prevent token limits
- **Serializable Data**: All data structures are converted to JSON-compatible format
- **Error Handling**: Robust error handling for API calls and file operations

### Quality Assurance
- **Statistical Validation**: Automatic assumption checking
- **Data Quality Checks**: Missing data detection and reporting
- **Methodological Rigor**: Integration of statistical best practices

### Scalability
- **Modular Design**: Each agent operates independently
- **Configurable Parameters**: Adjustable analysis depth and scope
- **Extensible Architecture**: Easy to add new agents or modify existing ones

## Dependencies

### Core Libraries
- **CrewAI**: Multi-agent framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **SciPy**: Statistical functions
- **Matplotlib/Seaborn**: Visualization
- **OpenAI**: LLM integration for insight generation

### Specialized Libraries
- **Sentence Transformers**: Embedding generation for RAG
- **FAISS**: Vector similarity search
- **PyYAML**: Configuration management

## Configuration

### Environment Variables
```bash
ULTRASAFE_API_KEY='your_ultrasafe_key_here'
```

### Directory Structure
```
analysis_agent/
├── agents/           # Agent implementations
├── knowledge_base/   # Statistical methods and best practices
├── prompts/         # LLM prompt templates
├── insights/        # Generated reports
├── visualizations/  # Generated charts
└── sample_data/     # Input datasets
```

## Usage Example

```python
# Run complete analysis pipeline
python main.py

# Expected outputs:
# - insights/insight_report_YYYYMMDD_HHMMSS.md
# - visualizations/top_5_problems.png
# - visualizations/[additional_plots].png
```

## Best Practices

1. **Data Quality**: Always validate input data before analysis
2. **Statistical Rigor**: Check assumptions before applying statistical tests
3. **Visualization**: Use appropriate chart types for different data types
4. **Documentation**: Maintain clear documentation of analysis decisions
5. **Version Control**: Use timestamps for output file management
6. **Error Handling**: Implement robust error handling for production use

## Extensibility

The system is designed for easy extension:
- **New Agents**: Add new agent classes following the existing pattern
- **New Data Types**: Modify agents to handle different data structures
- **Custom Visualizations**: Extend visualization agent with new plot types
- **Additional Knowledge**: Expand knowledge base with domain-specific content 