# InsightForge – CRISP-DM Project Log

> 📘 This is a living document based on the CRISP-DM methodology. It will be updated continuously as the project progresses through each phase.

---

## 1. Business Understanding

### 1.1 Project Objectives
- Build an intelligent assistant to monitor and extract strategic information from 5 LATAM financial companies:
  - Nubank, Ualá, Banco Santander México, Davivienda, BAC Credomatic.
- Detect key business signals: product launches, expansions, regulatory changes, and competitive moves.
- Deliver insights through an interactive dashboard using AI technologies (agents, embeddings, RAG, LLMs).

### 1.2 Business Success Criteria
- Weekly summaries or alerts with relevant updates.
- Automated detection of high-impact events.
- Scalable and modular backend with good documentation.

### 1.3 Situation Assessment

The current process of monitoring competitors in the LATAM financial sector is manual and scattered across various sources (news portals, company websites, reports, etc.). This makes it time-consuming, reactive, and limited in scope.

The objective of this project is to centralize and automate this process using AI, enabling faster and deeper strategic analysis.

Key constraints:
- Limited availability of structured data.
- Varying frequency and quality of information across companies.
- Need to balance automation with reliability.

### 1.4 Data Mining Goals

- Apply natural language processing to extract strategic events from unstructured text (news, blog posts).
- Generate vector embeddings to support semantic similarity search and retrieval.
- Classify content by relevance using rule-based or supervised methods.
- Develop agents that can route tasks, validate inputs, and interface with APIs.

---

## 2. Data Understanding

### 2.1 Data Sources

#### 2.1.1 Nubank

There is not a RSS or API to obtain these Nubank' news, so the information process has to be obtained through a standard web scrapping process.

Nubank has an official site where all the relevant company news are publish [text](https://international.nubank.com.br/es/files/), which makes it easier to obtain the news links for a long period of time. The srapping process is relatevly simple and there is no dynamic content, which simplifies the process.

Each of the news sites contains a title, a short summary explaining what the news is about, date of the article and the text. Initially, the first paragraph contains good information of what the articile is about and is good companing for the summary of the article.


### 2.2 Initial Observations
- [ ] Example: Nubank website has frequent blog/news updates.
- [ ] RSS feeds available for some banks, but others will require scraping.
- [ ] Central Bank APIs need authentication and parameter formatting.

---

## 3. Data Preparation

### 3.1 Planned Steps
- Collect news and company announcements.
- Normalize text (lowercase, remove stopwords, clean HTML).
- Use Named Entity Recognition (NER) for company names and dates.
- Preprocess for embeddings and similarity search.

### 3.2 Tools & Libraries
- `requests`, `BeautifulSoup`, `pandas`, `spaCy`, `langchain`, `datetime`, `re`

### 3.3 Notes
- [ ] Example: Davivienda uses dynamic content; may need Selenium or alternative strategy.

---

## 4. Modeling

### 4.1 AI/LLM Tasks
- Summarization of news articles.
- Classification of event relevance.
- Embedding generation + similarity for retrieval.

### 4.2 Agents Architecture
- Agent: Extracts key data from user query.
- Agent: Chooses correct country-specific data source.
- Agent: Queries APIs or scrapers.
- Agent: Validates inputs and fills missing parameters.
- Orchestrator: Manages routing between agents.

### 4.3 Initial Tests
- [ ] Run test queries through orchestrator
- [ ] Test vector search pipeline

---

## 5. Evaluation

### 5.1 Metrics
- Precision / recall for classification tasks.
- Accuracy of named entities extracted (companies, products, dates).
- Human feedback on quality of summaries and alerts.

### 5.2 Current Feedback
- [ ] To be added after first iteration

---

## 6. Deployment

### 6.1 Planned Stack
- Frontend: Streamlit or Gradio dashboard
- Backend: Python scripts with cron jobs or FastAPI
- Infrastructure: GitHub + local execution (phase 1), cloud automation (phase 2)

### 6.2 Automation Plans
- [ ] Daily or weekly data refresh
- [ ] Auto-generation of reports/alerts
- [ ] Slack or Telegram integration for alerts (optional)

---

## Appendix

### Companies Monitored
| Company            | Type       | Country                  |
|--------------------|------------|---------------------------|
| Nubank             | Fintech    | Brazil, Mexico, Colombia |
| Ualá               | Fintech    | Argentina, Mexico        |
| Banco Santander MX | Bank       | Mexico                   |
| Davivienda         | Bank       | Colombia, Central America|
| BAC Credomatic     | Bank       | Central America          |

### Keywords for Monitoring (initial)
- "launch", "new product", "investment", "expansion", "merger", "crypto", "wallet", "digital", "open banking", "partnership", etc.

---

### Changelog
- ✅ 2025-06-15: Document structure created. Added business understanding and preliminary data sources.
- ⏳ Next: Document agent architecture and prepare sample data flows.
