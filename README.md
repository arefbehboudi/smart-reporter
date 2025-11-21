# 📊 Jira Insight Deck
### _AI-powered automated reporting & slide generation for Jira_

Jira Insight Deck is an intelligent automation tool that reads data from Jira, analyzes it, and automatically generates **executive-ready reports** and **PowerPoint slides**.

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
git clone https://github.com/your-org/jira-insight-deck.git
cd jira-insight-deck
pip install -r requirements.txt
````

---

## 🔧 Configuration

Create a `.env` file:

```
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email
JIRA_API_TOKEN=your-api-token
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
jira-insight-deck/
├── src/
│   ├── jira_client.py        # Jira API integration
│   ├── analyzer.py           # Analysis engine
│   ├── summarizer.py         # LLM summary generator
│   ├── slide_builder.py      # PowerPoint builder
│   ├── config.py             # Settings
│   └── utils/                # Helpers
│
├── generate_report.py        # Entry point
├── requirements.txt
├── README.md
└── example-output/           # Sample results
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
