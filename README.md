# 📊 Smart Reporter
### _AI-powered automated reporting & slide generation_

Insight Deck is an intelligent automation tool that reads data, analyzes it, and automatically generates **executive-ready reports** and **PowerPoint slides**.

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
│   ├── core/                          # Core logic of the reporting engine
│   │   ├── jira_client.py             # Handles communication with Jira API (fetch issues, sprints, epics)
│   │   ├── analyzer.py                # Data analysis: grouping, progress calculation, blockers, metrics
│   │   ├── summarizer.py              # LLM-based summary generation (executive-level insights)
│   │   ├── slide_builder.py           # Builds PowerPoint slides using python-pptx
│   │   └── report_generator.py        # Orchestrates the full pipeline (fetch → analyze → summarize → slides)
│   │
│   ├── models/                        # Pydantic data models
│   │   ├── issue.py                   # Issue model
│   │   ├── epic.py                    # Epic model
│   │   ├── summary.py                 # Summary/insight output model
│   │   └── config_model.py            # Environment & config schema
│   │
│   ├── utils/                         # Utility helpers
│   │   ├── logger.py                  # Project-wide logging
│   │   ├── formatter.py               # Formatting helpers for text/markdown
│   │   └── file_utils.py              # File handling utilities
│   │
│   ├── config.py                      # Loads and manages .env and settings
│   └── constants.py                   # Constants used throughout the project
│
├── templates/                         # Templates for reports & prompts
│   ├── slides/
│   │   └── default_template.pptx      # Base PowerPoint template
│   ├── prompts/
│   │   └── summary_prompt.txt         # LLM prompt for executive summary
│   └── html/
│       └── report_template.html       # Optional HTML dashboard template
│
├── example-output/                    # Example outputs for users
│   ├── sample-report.pptx
│   └── sample-summary.txt
│
├── tests/                             # Unit and integration tests
│
├── generate_report.py                 # CLI entry point to generate full report
├── requirements.txt                   # Python dependencies
├── .env.example                       # Example environment variables
├── .gitignore
└── README.md

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
