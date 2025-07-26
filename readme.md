# Table of Contents

1. [Introduction](#data-processing-and-visualization-rag-chatbot)
2. [Documentation](#documentation)
3. [Installation Guide](#installation-guide)
4. [Dataset Setup](#dataset-setup)
5. [Sample `.env` File](#sample-env-file)
6. [System Architecture](#system-architecture)
7. [Project Directory Structure](#project-directory-structure)
8. [Key Features](#key-features)

   
# Demo 

[![Watch the Demo Video](https://img.youtube.com/vi/ljjOtt2aoJs/0.jpg)](https://www.youtube.com/watch?v=EPO4Zj9Q9nA)



# Data Analysis and Insight Generation Agent System

This project implements a multi-agent system designed for analyzing complex datasets, generating actionable insights, and creating visualizations. The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant statistical methods and best practices, ensuring rigorous and high-quality analysis.

---

## Documentation

For a detailed guide on this project, refer to the guide:

**[Detailed Guide: Data Analysis and Insight Generation Agent System](https://deepwiki.com/akshar1277/Data-Analysis-and-Insight-Generation-Ai-Agent-Ultrasafe/2-system-architecture)**

---


## Installation Guide

### 1. **Clone the Repository**
```bash
git clone <repo-url>
cd Data-Analysis-and-Insight-Generation-Ai-Agent-Ultrasafe
```

### 2. **Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install Requirements**
```bash
pip install -r requirements.txt
```

### 4. **Run the Analysis Pipeline**
```bash
python main.py
```

# Dataset Setup

To run the analysis pipeline, follow these steps:

1. **Place your dataset (CSV file) in the `sample_data` directory.**

   **Example:**  
   `sample_data/Aircraft_Annotation_DataFile.csv`

2. **Update the file name in `main.py`.**

    ```bash
    # filepath: /home/bacancy/AI_ML/poc/analysis_agent_crew/main.py
    df = pd.read_csv("sample_data/<your_csv_file_name>.csv")
    ```

3. **Run the `main.py` script.**
    ```bash
    python main.py
    ```
4. **After execution**:

    - **Insights** will be generated in the `insights` directory.  
    - **Visualizations** will be saved in the `visualizations` directory.



## Sample `.env` File

Below is a sample `.env` file to configure the environment variables required for the project. Replace the placeholder values with your actual credentials and settings.

```properties
# Sample .env file
ULTRASAFE_API_KEY=your-ultrasafe-api-key
```


---

## System Architecture

The system follows a layered architecture with clear separation between orchestration, agent processing, knowledge retrieval, and external service integration:

![System Architecture](https://drive.google.com/uc?export=view&id=1aAhgbAakM-c2x3U0B06yZxDbXDJkK8el)

---


## Project Directory Structure

```
.
├── main.py                     # Main analysis pipeline
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── README_Agent_Capabilities.md # Agent capabilities documentation
├── README_RAG_Implementation.md # RAG implementation documentation
├── README_Example_Analyses.md  # Example analyses and quality assessment
├── agents/                     # Agent implementations
│   ├── data_exploration_agent.py
│   ├── statistical_analysis_agent.py
│   ├── visualization_agent.py
│   ├── insight_generation_agent.py
│   ├── rag_retriever.py
├── knowledge_base/             # Statistical methods and best practices
│   ├── assumptions.md
│   ├── best_practices.md
│   ├── statistical_methods.md
│   ├── stats_best_practices.txt
├── prompts/                    # LLM prompt templates
│   ├── llm_viz_prompt.yaml
│   ├── llm_insight_prompt.yaml
├── insights/                   # Generated insight reports
├── visualizations/             # Generated visualizations
├── sample_data/                # Input datasets
└── .gitignore                   # Git ignore rules
```

---

## Key Features

### 1. **Multi-Agent System**
- **Data Exploration Agent**:Identifies patterns, outliers, and data quality issues.
- **Statistical Analysis Agent**:Applies statistical methods and validates assumptions.
- **Visualization Agent**:Generates diverse and insightful visualizations.
- **Insight Generation Agent**:Produces actionable insights in Markdown format.


### 2. **RAG Integration**
- Retrieves relevant statistical methods and best practices from the knowledge base.
- Ensures analysis follows established guidelines.


### 3. **Visualization Generation**
- Creates bar charts, pie charts, scatter plots, heatmaps, and more.
- Automatically selects the most relevant plots based on data characteristics.



### 4. **Insight Report**
- Generates a professional Markdown report summarizing findings, visualizations, and recommendations.

---



## Notes

- Ensure the .env file is properly configured before running the project.
- Insights and visualizations are automatically saved in their respective directories.
- Use the FastAPI endpoints for dynamic data upload and retrieval.