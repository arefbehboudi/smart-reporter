# 📊 Smart Reporter
### _AI-powered automated reporting & slide generation_

Smart Reporter is an intelligent automation tool that reads data, analyzes it, and automatically generates **executive-ready reports** and **PowerPoint slides**.

No more manual status reporting.  
No more stitching issues into slides.  
This tool does it for you. ✨

---

## 🚀 Features

### 🔹 Jira Data Extraction
- Connects to Jira Cloud/Server  
- Supports JQL queries  
- Fetches Issues, Sprints, Epics, Components, Story Points

### 🔹 AI + Rule-based Analysis
Automatically identifies:
- High-focus Epics/Features  
- Blockers, risks, dependencies  
- Intelligent grouping (Bug / Feature / Priority / Component)  
- Sprint velocity and progress metrics  
    
### 🔹 Smart Executive Summary
Example outputs:
- “Major focus this week was on **Payment Refactor**.”  
- “Two blockers impacted this sprint.”  
- “40% of sprint load was Bugfix work.”  
- “Epic X is now **65% complete**.”

### 🔹 Automatic PowerPoint Generation
Generates slides using `python-pptx`:
- Summary  
- Key Achievements  
- Issues & Risks  
- Progress Overview  
- Next Steps  

Fully customizable template (branding, logos, colors).

### 🔹 Scheduled or Manual Execution
Supports:
- Cron  
- GitHub Actions  
- Jenkins  
- CLI execution  

---

## 🛠 Tech Stack

- Python 3.10+  
- Atlassian Jira REST API  
- GPT / Ollama / Local LLM  
- python-pptx  
- Pandas, Pydantic  
- (Optional) FastAPI  

---

## 📦 Installation

```bash
git clone https://github.com/arefbehboudi/smart-reporter.git
cd smart-reporter
pip install -r requirements.txt
python -m streamlit run src/dashboard/app.py
````

---

## 🔧 Configuration

Create a `.env` file:

```
OPENAI_API_KEY=your-openai-key
REPORT_OUTPUT_DIR=./reports
MODEL_NAME=gpt-4o-mini
```

---

## ▶️ Usage

### Generate full report (text + slides)

```bash
python generate_report.py
```

### Text-only summary

```bash
python generate_report.py --no-slides
```

### Example cron job (weekly report)

```
0 9 * * MON python /path/to/generate_report.py
```

---

## 📁 Project Structure

```
smart-reporter/
│
├── src/
│   ├── core/                                  # Core logic of the reporting engine
│   │   ├── clients/                           # Data source clients (Jira, etc.)
│   │   │   ├── __init__.py
│   │   │   ├── base_client.py                 # Abstract interface for all clients
│   │   │   ├── jira_client.py                 # Jira implementation of BaseClient
│   │   │   ├── github_client.py               # GitHub Issues client
│   │   │   └── linear_client.py               # Linear client
│   │   │
│   │   ├── pipelines/                         # High-level reporting pipelines
│   │   │   ├── __init__.py
│   │   │   ├── sprint_report_pipeline.py      # Sprint-based report pipeline
│   │   │   └── epic_report_pipeline.py        # Epic/feature-based report pipeline
│   │   │
│   │   ├── services/                          # Service layer (used by CLI / dashboard / API)
│   │   │   ├── __init__.py
│   │   │   ├── analysis_service.py            # High-level analysis functions
│   │   │   ├── reporting_service.py           # Orchestrates full report generation
│   │   │   └── template_service.py            # Handles templates, branding, variants
│   │   │
│   │   ├── analyzer.py                        # Data analysis: grouping, progress, blockers, metrics
│   │   ├── summarizer.py                      # LLM-based summary generation (executive-level insights)
│   │   ├── slide_builder.py                   # Builds PowerPoint slides using python-pptx
│   │   └── report_generator.py                # Legacy/simple orchestrator (can wrap pipelines/services)
│   │
│   ├── models/                                # Pydantic data models
│   │   ├── __init__.py
│   │   ├── issue.py                           # Issue model
│   │   ├── epic.py                            # Epic/feature model
│   │   ├── sprint.py                          # Sprint & sprint metrics model
│   │   └── summary.py                         # Summary/insight output model
│   │
│   │
│   ├── utils/                                 # Utility helpers
│   │   ├── __init__.py
│   │   ├── logger.py                          # Project-wide logging setup
│   │   ├── formatter.py                       # Formatting helpers for text/markdown
│   │   ├── file_utils.py                      # File handling utilities and paths
│   │   └── charts.py                          # Chart/plot helpers (for PPT and dashboard)
│   │
│   ├── dashboard/                             # Streamlit dashboard (or other UI frontends)
│   │   ├── __init__.py
│   │   ├── app.py                             # Streamlit entry point
│   │   ├── components/                        # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── metrics_panel.py               # Top-level KPIs (velocity, blockers, etc.)
│   │   │   ├── filters_panel.py               # Filters (team, sprint, JQL)
│   │   │   └── issues_table.py                # Issues / blockers tables
│   │   ├── charts/                            # Dashboard-specific charts
│   │   │   ├── __init__.py
│   │   │   ├── velocity_chart.py
│   │   │   ├── workload_chart.py
│   │   │   └── epic_progress_chart.py
│   │   └── utils.py                           # Dashboard helpers (caching, session state, etc.)
│   │
│   ├── api/                                   # Optional: API layer (FastAPI or similar)
│   │   ├── __init__.py
│   │   └── server.py                          # HTTP API for generating reports programmatically
│   │
│   ├── config.py                              # Loads and manages .env and settings (wraps config_model)
│   ├── constants.py                           # Constants used throughout the project
│   └── __init__.py
│
├── templates/                                 # Templates for reports & prompts
│   ├── slides/
│   │   ├── default_template.pptx              # Base PowerPoint template
│   │   ├── minimal_template.pptx              # Minimal, clean template
│   │   └── corporate_template.pptx            # Enterprise / branded template
│   │
│   ├── prompts/
│   │   ├── summary_prompt.txt                 # LLM prompt for executive summary
│   │   └── risk_prompt.txt                    # (optional) prompt for risks/blockers analysis
│   │
│   └── html/
│       ├── report_template.html               # Optional HTML dashboard/report template
│       └── sprint_dashboard.html              # Optional HTML sprint overview
│
├── assets/                                    # Static assets (branding)
│   ├── logos/
│   │   └── company_logo.png
│   ├── icons/
│   └── fonts/
│
├── outputs/                                   # Generated outputs (gitignored)
│   ├── reports/                               # Generated PPTX / HTML / PDF reports
│   ├── summaries/                             # Generated text/markdown summaries
│   ├── logs/                                  # Log files
│   └── cache/                                 # Temporary caches (JSON, pickle, etc.)
│
├── example-output/                            # Example outputs for users
│   ├── sample-report.pptx
│   └── sample-summary.txt
│
├── tests/                                     # Unit and integration tests
│   ├── unit/
│   │   ├── test_jira_client.py
│   │   ├── test_analyzer.py
│   │   ├── test_summarizer.py
│   │   ├── test_slide_builder.py
│   │   └── test_services.py
│   └── integration/
│       └── test_full_pipeline.py
│
├── scripts/                                   # Helper scripts (optional)
│   ├── run_report.sh
│   └── run_dashboard.sh
│
├── generate_report.py                         # CLI entry point to generate full report
├── run_dashboard.py                           # Simple entry point for Streamlit dashboard
├── requirements.txt                           # Python dependencies
├── pyproject.toml                             # (optional) Modern build/config
├── .env.example                               # Example environment variables
├── .gitignore
├── README.md
└── LICENSE

```

---

## 🧩 Roadmap

* [ ] Multiple PPT templates
* [ ] HTML dashboard mode
* [ ] PR insights (GitHub/GitLab)
* [ ] SaaS version
* [ ] Slack/Teams integration

---

## 🤝 Contributing

Contributions are welcome.
For major changes, please open an issue to discuss the proposal first.

---

## 📄 License

MIT License
