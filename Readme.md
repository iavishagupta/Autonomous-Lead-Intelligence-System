# 🤖 Autonomous Lead Intelligence System

An AI-powered multi-agent system that automates lead discovery, qualification, scoring, and personalized email generation.

This project demonstrates how autonomous agent workflows can transform raw lead data into structured insights and high-quality outreach emails with minimal human intervention.

---

## 📘 Table of Contents

- Overview  
- System Architecture  
- Workflow Pipeline  
- Execution Flow  
- Agents & Responsibilities  
- YAML Configuration  
- Data Flow  
- Tech Stack  
- Project Structure  
- Setup Instructions  
- Running the Project  
- Example Flow  
- Future Improvements  
- License  

---

## 🌐 Overview

The **Autonomous Lead Intelligence System** automates the full lead intelligence lifecycle:

- Collect and analyze lead data  
- Evaluate cultural and strategic fit  
- Score and validate leads  
- Generate personalized outreach emails  

The system is built using modular AI agents coordinated through a structured pipeline.

---

## 🧠 System Architecture

The system is divided into two main pipelines:

### 1. Lead Qualification Pipeline
- Data collection  
- Cultural fit analysis  
- Lead scoring and validation  

### 2. Email Engagement Pipeline
- Email drafting  
- Engagement optimization  

Both pipelines operate independently and are orchestrated through a central Flow controller.

---

## 🔄 Workflow Pipeline

```
Input Leads (JSON)
        ↓
Lead Data Collection
        ↓
Cultural Fit Analysis
        ↓
Lead Scoring & Validation
        ↓
Filter High-Quality Leads (>70)
        ↓
Email Drafting
        ↓
Engagement Optimization
        ↓
Final Email Output
```

---

## 🔁 Execution Flow (Core Pipeline)

The system uses a Flow-based orchestration to process leads step-by-step:

```
Fetch Leads → Score Leads → Filter Leads → Generate Emails → Output
```

### Pipeline Breakdown

1. **Fetch Leads**
   - Loads lead data from `lead_data.json`

2. **Score Leads**
   - Runs Lead Qualification Crew
   - Collects structured outputs (Pydantic models)
   - Saves results to `lead_scores.json`

3. **Filter Leads**
   - Filters leads with score > 70
   - Stores results in `filtered_leads.json`

4. **Generate Emails**
   - Runs Email Engagement Crew
   - Generates personalized emails
   - Attaches email content to each lead

5. **Final Output**
   - Ready-to-send emails
   - Structured JSON with enriched lead data

---

## 🧑‍🤝‍🧑 Agents & Responsibilities

### Lead Qualification Agents

- **Lead Data Specialist**
  - Collects personal and company data  

- **Cultural Fit Analyst**
  - Evaluates alignment with company values  

- **Lead Scorer & Validator**
  - Calculates and validates final lead score  

---

### Email Engagement Agents

- **Email Content Writer**
  - Writes concise, personalized email drafts  

- **Engagement Optimization Specialist**
  - Enhances emails with CTAs and engagement hooks  

---

## ⚙️ YAML Configuration

### Email Engagement Agents

```yaml
email_content_specialist:
  role: Email Content Writer
  goal: Write a concise, personalized follow-up email using lead info.

engagement_strategist:
  role: Engagement Optimization Specialist
  goal: Improve the draft with strong CTAs and engagement hooks.
```

---

### Email Tasks

```yaml
email_drafting:
  description: Write a personalized follow-up email using lead data.
  expected_output: Concise email under 120 tokens

engagement_optimization:
  description: Optimize email with strong CTAs and hooks
  expected_output: Final email under 150 tokens
```

---

### Lead Qualification Agents

```yaml
lead_data_collector:
  role: Lead Data Specialist

cultural_fit_analyzer:
  role: Cultural Fit Analyst

scorer_validator:
  role: Lead Scorer and Validator
```

---

## 📂 Data Flow

- `lead_data.json` → Input leads  
- `lead_scores.json` → Scored leads  
- `filtered_leads.json` → Qualified leads + generated emails  

---

## 🧰 Tech Stack

- Python  
- CrewAI (agent orchestration)  
- YAML (agent/task configuration)  
- Serper API (search)  
- Web Scraping (BeautifulSoup / Requests)  
- Pydantic (structured outputs)  

---

## 📁 Project Structure

```
Autonomous-Lead-Intelligence-System/
│
├── yamlFiles/
│   ├── email_engagement_agents.yaml
│   ├── email_engagement_tasks.yaml
│   ├── lead_qualification_agents.yaml
│   ├── lead_qualification_tasks.yaml
│
├── lead_qualification_crew.py
├── email_engagement_crew.py
├── ASIL.py
│
├── lead_data.json
├── lead_scores.json
├── filtered_leads.json
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/iavishagupta/Autonomous-Lead-Intelligence-System.git
cd Autonomous-Lead-Intelligence-System
```

---

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Set Environment Variables

```
export SERPER_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here
```

---

## ▶️ Running the Project

```
python ASIL.py
```

This executes the full autonomous pipeline.

---

## 📊 Example Flow

**Input:**
```
Lead data (company, CEO, email)
```

**Output:**
- Lead score (0–100)  
- Cultural fit analysis  
- Filtered high-quality leads  
- Personalized outreach emails  

---

## 🔮 Future Improvements

- Multi-agent collaboration enhancements  
- CRM integration  
- UI/dashboard for visualization  
- Email sending automation  
- Improved scoring models  

---

## 📄 License

This project is open-source and available under the MIT License.
