import os
from dotenv import load_dotenv
from crewai import Crew
from crewai.process import Process
from langchain_openai import ChatOpenAI
from agents import Agents
from tasks import Tasks

load_dotenv()
os.environ["OPENAI_MODEL_NAME"] = "gpt-5-mini" # gpt-5-mini-2025-08-07


agents = Agents()
tasks = Tasks()

researcher = agents.researcher()
technical_analyst = agents.technical_analyst()
financial_analyst = agents.financial_analyst()
hedge_fund_manager = agents.hedge_fund_manager()

research_task = tasks.research(researcher)
technical_task = tasks.technical_analysis(technical_analyst)
financial_task = tasks.financial_analysis(financial_analyst)
recommend_task = tasks.investement_recommendation(
    hedge_fund_manager,
    [
        research_task,
        technical_task,
        financial_task,
    ]
)

crew = Crew(
    agents=[
        researcher,
        technical_analyst,
        financial_analyst,
        hedge_fund_manager,
    ],
    tasks=[
        research_task,
        technical_task,
        financial_task,
        recommend_task,
    ],
    verbose=True,
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-5-mini", temperature=1.0),
    memory=True,
)

result = crew.kickoff(
    inputs=dict(
        company="Tesla"
    )
)