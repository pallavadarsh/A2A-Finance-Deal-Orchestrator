# 🤝 A2A (Agent-to-Agent) Protocol Demo  
**Investment Banking + TechOps with Human-in-the-Loop**

This project demonstrates a **true microservices-based Agent-to-Agent (A2A) protocol** using [FastAPI](https://fastapi.tiangolo.com/), [LangGraph concepts](https://www.langchain.com/langgraph), and an optional [LLM (Groq)](https://groq.com/).  
It is designed for **executive demos** (banking use cases) and **technical labs** (infra, diagnostics, risk).  

---

## 🌟 Key Features
- **True Agent-to-Agent (A2A) Protocol**  
  Each agent is an independent FastAPI microservice exposing `/a2a/message`.  
  Messages follow a strict protocol:  
  ```json
  {
    "sender": "FinanceAgent",
    "recipient": "RiskAgent",
    "type": "PROPOSE",
    "payload": {...},
    "corr_id": "...",
    "in_reply_to": "..."
  }
  ```

- **Domain Agents**  
  - FinanceAgent → computes valuation multiples.  
  - RiskAgent → assesses risk, requests diagnostics/security.  
  - LegalAgent → adds clauses & compliance flags.  
  - DiagnosticsAgent → reports incidents/root causes.  
  - InfraAgent → proposes remediation.  
  - SecurityAgent → recommends controls.  
  - CommitteeAgent → drafts & finalizes memos (LLM-enabled).  

- **Human-in-the-Loop (HITL)**  
  A reviewer can approve or revise before final memo generation.  

- **Traceability & Logs**  
  Every message is logged in orchestrator and viewable via API or React UI.  

- **UI with Wow Factor**  
  A React + MUI dashboard shows:  
  - Deal input & memos (draft/final).  
  - Live trace timeline with protocol badges (PROPOSE, REQUEST, INFORM, ADVISE, HUMAN_APPROVE, etc.).

---

## 🏗 Architecture
```
[React UI] <—> [Orchestrator API]
                      |
          ┌───────────┴───────────┐
   [Finance] [Risk] [Legal] [Diagnostics]
          |       |       |
       [Infra] [Security] [Committee (LLM)]
```

- Orchestrator = router + tracer (not a brain).  
- Agents decide next steps and communicate via A2A protocol.  
- CommitteeAgent optionally calls Groq LLM for natural-language memos.  

---

## 🚀 Quickstart

### 1. Clone Repo
```bash
git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>
```

### 2. Start Backend (Agents + Orchestrator)
With Docker Compose:
```bash
docker compose up --build
```

Services:
- Orchestrator → `http://localhost:8010`  
- Finance → `8101` | Risk → `8102` | Legal → `8103`  
- Diagnostics → `8104` | Infra → `8105` | Security → `8106` | Committee → `8107`  

### 3. Start Frontend (React + MUI UI)
```bash
cd a2a-frontend
npm install --legacy-peer-deps
npm start
```
Open [http://localhost:3000](http://localhost:3000).

---

## 📡 API Usage

### Kick off a Deal
```bash
curl -X POST http://localhost:8010/deal/start -H "Content-Type: application/json" -d '{
  "deal_name": "Project Falcon",
  "target": {"name": "Acme FinTech", "sector": "FinTech", "region": "APAC"},
  "financials": {"revenue": 120.0, "ebitda": 24.0, "debt": 30.0},
  "purchase_price": 220.0,
  "currency": "USD"
}'
```

### Human Review
```bash
curl -X POST http://localhost:8010/deal/review -H "Content-Type: application/json" -d '{
  "run_id": "<RID>",
  "decision": "approve",
  "feedback": "Add SOC2 compliance note"
}'
```

### View Timeline
```bash
curl http://localhost:8010/trace/<RID>/timeline
```

---

## 🤖 LLM Integration
- **CommitteeAgent** can use Groq LLMs to draft/finalize memos.  
- Enable by setting env vars when running CommitteeAgent:  
  ```bash
  export GROQ_API_KEY=your_api_key
  export GROQ_MODEL=llama-3.1-8b-instant
  ```

If no key is set → falls back to mock memos.

---

## 🔎 Example Trace
```
FinanceAgent —PROPOSE→ RiskAgent | {'valuation': {'ev_ebitda': 9.17, 'price': 220.0}}
RiskAgent —REQUEST→ DiagnosticsAgent | {'check': 'latency'}
LegalAgent —ADVISE→ CommitteeAgent | {'clauses': ['MAC', 'Compliance']}
...
CommitteeAgent —INFORM→ Orchestrator | {'draft_memo': 'Draft investment memo ...'}
HumanReviewer —HUMAN_APPROVE→ CommitteeAgent | {'notes': 'Demo feedback'}
CommitteeAgent —INFORM→ Orchestrator | {'final_memo': 'Final investment memo ...'}
```

---

## 🧑‍💻 Use Cases
- **Banking Demo** → Investment memo pipeline with LLM summaries + human approval.  
- **TechOps Demo** → Infra diagnostics, remediation proposals, risk scoring without LLM.  

---

## 📜 License
MIT (or your org’s license)
