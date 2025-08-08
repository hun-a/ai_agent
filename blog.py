import os
from crewai import Crew, Agent, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv
from models import BlogPost

load_dotenv()

os.environ["OPENAI_MODEL_NAME"] = "gpt-5-mini" # gpt-5-mini-2025-08-07

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

researcher = Agent(
    role="Senior Researcher",
    goal="Search the web, extract and analyze information.",
    backstory="""
    You produce the highest quality research possible.
    You use multiple sources of information and you always double check
    your sources to make sure they are true and up to date.
    You want to impress your coworkers with your work.
    """,
    allow_delegation=False,
    verbose=True,
    tools=[
        search_tool,
        scrape_tool,
    ],
    max_iter=10,
)

editor = Agent(
    role="Senior Writer/Editor",
    goal="Write engaging blog posts",
    backstory="""
    You write content that keeps people engaged and entertained.
    Your content is easy to read it is informative and it makes people want to
    share it with their friends.
    You are working for a very important client.
    """,
    verbose=True,
)

task = Task(
    description="Write a blog post about {topic}",
    agent=editor,
    expected_output="""
    A blog post with an introduction,
    at least three sub-sections of content, linkks to sources,
    a set of suggested hashtags for social media and a catchy title.
    """,
    output_file="blog_post.json",
    output_pydantic=BlogPost,
)

crew = Crew(agents=[researcher, editor], tasks=[task], verbose=True)

result = crew.kickoff(
    inputs=dict(
        topic="The biggest box office flops of 2024"
    )
) 