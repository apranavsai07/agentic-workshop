# Multi-Agent AI Hackathon Ideator Workshop

Build a simple collaborative AI system with **CrewAI** and **Google Gemini**.

This workshop introduces students to a multi-agent workflow. Two AI agents work together:

1. **Product Architect** researches a project idea and proposes practical features.
2. **Technical Architect (CTO)** converts those ideas into a technical blueprint.

The final result is saved as `Hackathon_Elite_Blueprint.md`.

---

## 1. Project structure

```text
agentic-workshop/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

The generated Markdown blueprint appears in the project folder after a successful run.

## 2. Requirements

- Python 3.10 or newer
- Internet connection
- Google Gemini API key
- VS Code or another code editor

## 3. Clone the repository

On the GitHub repository page, select **Code**, copy the repository URL, and run:

```bash
git clone YOUR_REPOSITORY_URL
cd agentic-workshop
```

Replace `YOUR_REPOSITORY_URL` with the URL of your own repository.

## 4. Create and activate a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 5. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Configure your Gemini API key

1. Open [Google AI Studio](https://aistudio.google.com/).
2. Create or copy a Gemini API key.
3. In the project folder, copy `.env.example` and rename the copy to `.env`.
4. Add your API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini/gemini-2.5-flash
```

**Keep your API key private. Never commit `.env` to GitHub.**

If the model name is unavailable for your account or region, use a currently supported Gemini model name in `GEMINI_MODEL`.

## 7. Run the workshop

```bash
python app.py
```

When the workflow finishes, the application creates:

```text
Hackathon_Elite_Blueprint.md
```

Open the file in VS Code and press:

- **Windows/Linux:** `Ctrl + Shift + V`
- **macOS:** `Cmd + Shift + V`

This opens the rendered Markdown preview.

---

## 8. How the multi-agent system works

```text
                 Project Problem
                        |
                        v
             +----------------------+
             |   Product Architect  |
             |  Research and ideas  |
             +----------------------+
                        |
                 Product analysis
                        |
                        v
             +----------------------+
             |          CTO         |
             | Architecture and plan|
             +----------------------+
                        |
                        v
             +----------------------+
             |   Markdown Blueprint|
             +----------------------+
```

### Agent 1: Product Architect

- Understands the problem statement.
- Searches for relevant existing approaches.
- Identifies gaps and limitations.
- Suggests three practical features.
- Recommends a minimum viable prototype.

### Agent 2: CTO

- Uses the Product Architect's output.
- Selects a suitable technology stack.
- Explains the system architecture.
- Creates a 24-hour development plan.
- Describes a demo scenario and project impact.

### Orchestration

The project uses `Process.sequential`. This means the Product Architect's task runs first. The CTO task then receives the first task's output through its context.

---

## 9. Understanding the five code sections

| Section | Purpose |
|---|---|
| Configuration | Loads the API key and checks settings |
| Core Brain | Connects CrewAI to Google Gemini |
| Execution Tool | Gives the Product Architect web-search capability |
| Agents and Tasks | Defines agent roles, prompts, and deliverables |
| Orchestration | Runs tasks in sequence and saves the result |

`verbose=False` keeps the terminal output compact. `memory=False` avoids persistent-memory setup because this example only needs task-to-task context during one run.

## 10. Customize the project

Students can build their own ideator by changing `PROBLEM_STATEMENT` in `app.py`.

Example topics:

- Smart traffic management
- AI-powered crop disease detection
- Smart waste management
- Personal finance assistant
- Energy monitoring for buildings
- AI-based student study planner

For best results, write a specific problem statement. Include the target users, the problem they face, and the outcome the solution should provide.

## 11. Troubleshooting

### `GEMINI_API_KEY was not found`

- Check that the file is named `.env`, not `.env.txt`.
- Confirm that `.env` is in the same folder as `app.py`.
- Check that the key is assigned as `GEMINI_API_KEY=...`.
- Do not add quotes unless your key requires them.

### Gemini authentication or model error

- Check that the API key is valid.
- Confirm that the selected model is available to your API key.
- Update `GEMINI_MODEL` in `.env` to a supported Gemini model identifier.

### Web search is unavailable

The workflow is designed to continue if web search fails. The Product Architect is instructed to label unverified background knowledge and not invent sources or statistics.

### Package installation error

Make sure the virtual environment is active, then run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 12. GitHub safety checklist

Before pushing the project:

- [ ] `.env` contains your real key locally only.
- [ ] `.env` is listed in `.gitignore`.
- [ ] No API key is hard-coded in `app.py`.
- [ ] `venv/` is not included in the repository.
- [ ] Test the project from a fresh virtual environment.

Example Git commands:

```bash
git init
git add app.py requirements.txt README.md .env.example .gitignore
git commit -m "Add CrewAI multi-agent workshop project"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

---

## Learning outcome

By completing this workshop, students will understand how to:

- Connect an LLM to CrewAI.
- Define specialized AI agents.
- Give agents tools.
- Create tasks with clear prompts and expected outputs.
- Pass task results between agents.
- Orchestrate agents sequentially.
- Generate a useful Markdown artifact from an AI workflow.
