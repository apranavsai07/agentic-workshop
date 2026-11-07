
"""
MULTI-AGENT AI HACKATHON IDEATOR
CrewAI + Google Gemini

Agent 1: Product Architect
Agent 2: Technical Architect (CTO)

Both agents collaborate to generate a project blueprint.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from ddgs import DDGS

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box


# ============================================================
# 1. CONFIGURATION
# ============================================================

load_dotenv()

console = Console()

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini/gemini-3.8-flash"
)

OUTPUT_FILE = "Hackathon_Elite_Blueprint.md"

PROBLEM_STATEMENT = (
    "Smart water management and automated leakage detection "
    "for urban housing societies."
)


def show_header():

    console.print()

    console.print(
        Panel(
            "[bold white]MULTI-AGENT AI HACKATHON IDEATOR[/bold white]\n"
            "[cyan]CrewAI  |  Google Gemini  |  Web Search[/cyan]\n\n"
            f"[white]Project: {PROBLEM_STATEMENT}[/white]",

            title="[bold cyan]WORKSHOP PROJECT[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2)
        )
    )


def validate_api_key():

    if not API_KEY:

        console.print(
            Panel(
                "[bold red]Gemini API key not found![/bold red]\n\n"
                "Create a .env file and add:\n"
                "GEMINI_API_KEY=your_api_key_here",

                title="Configuration Error",
                border_style="red"
            )
        )

        sys.exit(1)


validate_api_key()


# ============================================================
# 2. CORE BRAIN - GOOGLE GEMINI
# ============================================================

llm = LLM(
    model=MODEL_NAME,
    api_key=API_KEY,

)


# ============================================================
# 3. EXECUTION TOOL - WEB SEARCH
# ============================================================

@tool("Web Search")
def web_search(search_query: str) -> str:
    """
    Searches the web for existing solutions,
    technologies and relevant project information.
    """

    try:

        results = list(
            DDGS().text(search_query, max_results=4) or []
        )

        if not results:

            return (
                "No search results found. "
                "Continue using general technical knowledge. "
                "Do not invent sources or statistics."
            )

        output = []

        for index, item in enumerate(results, start=1):

            output.append(
                f"{index}. {item.get('title', 'Untitled')}\n"
                f"URL: {item.get('href', '')}\n"
                f"Summary: {item.get('body', '')}"
            )

        return "\n\n".join(output)

    except Exception as error:

        return (
            "Web search is temporarily unavailable. "
            f"Error: {type(error).__name__}. "
            "Do not invent sources or statistics."
        )


# ============================================================
# 4. AGENT 1 - PRODUCT ARCHITECT
# ============================================================

product_architect = Agent(

    role="Product Architect",

    goal=(
        "Analyze the project problem, identify existing limitations "
        "and propose three practical and innovative features."
    ),

    backstory="""
    You are an experienced product architect and hackathon mentor.

    You specialize in converting real-world problems into
    practical software and AI solutions.

    You focus on:
    - Real-world usefulness
    - Affordable technologies
    - Practical implementation
    - Student-friendly demonstrations

    Avoid unnecessary complexity and unrealistic technologies.
    """,

    tools=[web_search],

    llm=llm,

    verbose=False,

    memory=False,

    allow_delegation=False,

    max_iter=4
)


# ============================================================
# 5. AGENT 2 - CTO
# ============================================================

cto_agent = Agent(

    role="Technical Architect and CTO",

    goal=(
        "Convert the product architect's ideas into a complete "
        "and realistic technical project blueprint."
    ),

    backstory="""
    You are an experienced software architect and CTO.

    You specialize in selecting suitable technologies
    and designing practical software architectures.

    You explain technical concepts in simple language.

    Your responsibilities include:
    - Selecting the technology stack
    - Designing system architecture
    - Explaining the workflow
    - Preparing a development roadmap
    - Identifying project limitations

    Avoid unnecessary technical jargon and long explanations.
    """,

    llm=llm,

    verbose=False,

    memory=False,

    allow_delegation=False,

    max_iter=4
)


# ============================================================
# 6. TASK 1 - PRODUCT IDEATION
# ============================================================

task_ideation = Task(

    description=f"""
    Analyze the following project:

    PROJECT:
    {PROBLEM_STATEMENT}

    Use the Web Search tool to identify existing approaches
    and relevant technologies.

    Prepare a concise report with these sections:

    ## 1. Problem Analysis
    Explain the problem in 3 short bullet points.

    ## 2. Existing Solutions
    Explain common approaches and identify 3 limitations.

    If search fails, clearly mention that the information
    is based on general knowledge.

    ## 3. Proposed Solution
    Explain the proposed system in 3-4 sentences.

    ## 4. Three Innovative Features

    For each feature explain:
    - What it does
    - Technology used
    - How students can demonstrate it
    - Main benefit

    ## 5. Minimum Viable Product

    List the essential features needed for a working prototype.

    RULES:
    - Keep the response between 250 and 350 words.
    - Use short sentences.
    - Use clear headings and bullet points.
    - Recommend affordable technologies.
    - Avoid unrealistic or expensive technologies.
    - Do not invent research findings or statistics.
    """,

    expected_output="""
    A concise product analysis containing problem analysis,
    existing limitations, proposed solution, three practical
    features and minimum viable product.
    """,

    agent=product_architect
)


# ============================================================
# 7. TASK 2 - TECHNICAL ARCHITECTURE
# ============================================================

def create_architecture_task(product_report):

    return Task(

        description=f"""
        The following report was prepared by Agent 1,
        the Product Architect.

        YOUR INPUT FROM AGENT 1:
        {product_report}

        Your responsibility is to convert these ideas
        into a technical project blueprint.

        Follow this exact structure:

        # SMART WATER MANAGEMENT SYSTEM
        ## Hackathon Project Blueprint

        ## 1. Project Overview
        Explain the project in 3-4 sentences.

        ## 2. Main Features
        List the selected features and their benefits.

        ## 3. System Architecture
        Explain the main components.

        Include a simple architecture flow:

        Sensors -> Backend -> Database ->
        AI Detection -> Alerts -> Dashboard

        ## 4. Technology Stack

        Create a valid Markdown table:

        | Layer | Technology | Purpose |

        Include:
        - Frontend
        - Backend
        - Database
        - AI/ML
        - IoT
        - Notifications
        - Deployment

        ## 5. System Workflow

        Explain the workflow in 5-7 numbered steps.

        ## 6. 24-Hour Development Roadmap

        Create a valid Markdown table:

        | Time | Development Task | Deliverable |

        Divide the plan into six phases of four hours each.

        Keep the tasks realistic for students.

        ## 7. Demo Scenario

        Explain one demonstration that students can show to judges.

        ## 8. Expected Results and Limitations

        Explain what the prototype can demonstrate
        and what requires further testing.

        ## 9. Judge Impact

        Briefly explain innovation, feasibility and real-world value.

        ## 10. Future Improvements

        List up to four improvements.

        IMPORTANT RULES:

        - Keep the complete response between 450 and 600 words.
        - Use short sentences and simple English.
        - Use compact bullet points.
        - Create properly formatted Markdown tables.
        - Avoid unnecessary blank lines.
        - Do not repeat the same information.
        - Do not include Python code or execution logs.
        - Do not claim the project is production-ready.
        - Return the complete blueprint.
        """,

        expected_output="""
        A complete and concise Markdown technical blueprint
        with all ten sections, two valid tables,
        system architecture and a 24-hour roadmap.
        """,

        agent=cto_agent
    )


# ============================================================
# 8. HELPER - DISPLAY AGENT OUTPUT IN A BOX
# ============================================================

def display_agent_output(title, content):

    console.print()

    console.print(
        Panel(
            Markdown(content),

            title=f"[bold cyan]{title}[/bold cyan]",

            border_style="cyan",

            box=box.ROUNDED,

            padding=(1, 2),

            expand=True
        )
    )


# ============================================================
# 9. ORCHESTRATION - AGENT COLLABORATION
# ============================================================

def run_workshop():

    show_header()

    # --------------------------------------------------------
    # STEP 1: PRODUCT ARCHITECT
    # --------------------------------------------------------

    console.print(
        "\n[bold cyan]STEP 1/3 - PRODUCT ARCHITECT[/bold cyan]"
    )

    console.print(
        "[white]Agent 1 is analyzing the problem and searching "
        "for existing solutions...[/white]\n"
    )

    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]{task.description}"),
        console=console
    ) as progress:

        task = progress.add_task(
            "Product Architect is working...",
            total=None
        )

        product_crew = Crew(

            agents=[product_architect],

            tasks=[task_ideation],

            process=Process.sequential,

            verbose=False
        )

        product_result = product_crew.kickoff()

        progress.update(
            task,
            description="[bold cyan]Product Architect completed[/bold cyan]",
            total=1,
            completed=1
        )

    product_report = (
        getattr(product_result, "raw", None)
        or str(product_result)
    ).strip()

    display_agent_output(
        "AGENT 1 - PRODUCT ARCHITECT OUTPUT",
        product_report
    )

    console.print(
        "\n[dim]Agent 1 has completed its task. "
        "Its report will now be passed to Agent 2.[/dim]"
    )

    # --------------------------------------------------------
    # STEP 2: CTO AGENT
    # --------------------------------------------------------

    console.print(
        "\n[bold cyan]STEP 2/3 - TECHNICAL ARCHITECT (CTO)[/bold cyan]"
    )

    console.print(
        "[white]Agent 2 has received Agent 1's report. "
        "It is preparing the architecture and development plan...[/white]\n"
    )

    architecture_task = create_architecture_task(product_report)

    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]{task.description}"),
        console=console
    ) as progress:

        task = progress.add_task(
            "CTO is preparing the technical blueprint...",
            total=None
        )

        cto_crew = Crew(

            agents=[cto_agent],

            tasks=[architecture_task],

            process=Process.sequential,

            verbose=False
        )

        final_result = cto_crew.kickoff()

        progress.update(
            task,
            description="[bold cyan]CTO completed the blueprint[/bold cyan]",
            total=1,
            completed=1
        )

    final_blueprint = (
        getattr(final_result, "raw", None)
        or str(final_result)
    ).strip()

    # --------------------------------------------------------
    # STEP 3: SAVE AND DISPLAY FINAL OUTPUT
    # --------------------------------------------------------

    console.print(
        "\n[bold cyan]STEP 3/3 - GENERATING FINAL OUTPUT[/bold cyan]"
    )

    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]{task.description}"),
        console=console
    ) as progress:

        task = progress.add_task(
            "Saving the final blueprint...",
            total=None
        )

        if not final_blueprint:
            raise RuntimeError("The AI returned an empty blueprint.")

        Path(OUTPUT_FILE).write_text(
            final_blueprint + "\n",
            encoding="utf-8"
        )

        progress.update(
            task,
            description="[bold cyan]Blueprint saved successfully[/bold cyan]",
            total=1,
            completed=1
        )

    # Display complete final AI response in terminal
    display_agent_output(
        "FINAL PROJECT BLUEPRINT",
        final_blueprint
    )

    # --------------------------------------------------------
    # COMPLETION MESSAGE
    # --------------------------------------------------------

    console.print()

    console.print(
        Panel(
            "[bold white]WORKSHOP EXECUTION COMPLETED[/bold white]\n\n"
            "[cyan]Status:[/cyan] Success\n"
            f"[cyan]Output File:[/cyan] {OUTPUT_FILE}\n"
            f"[cyan]Generated:[/cyan] "
            f"{datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n\n"
            "[white]Open the Markdown file in VS Code.[/white]\n"
            "[dim]Press Ctrl + Shift + V to preview.[/dim]",

            border_style="cyan",

            box=box.ROUNDED,

            padding=(1, 2)
        )
    )


# ============================================================
# 10. MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    try:

        run_workshop()

    except Exception as error:

        console.print(
            Panel(
                f"[bold red]Execution failed[/bold red]\n\n"
                f"{type(error).__name__}: {error}\n\n"
                "Check your API key, internet connection "
                "and installed packages.",

                title="ERROR",

                border_style="red"
            )
        )

        sys.exit(1)
