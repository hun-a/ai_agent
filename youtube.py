import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, YoutubeChannelSearchTool

load_dotenv()

os.environ["OPENAI_MODEL_NAME"] = "gpt-5-mini" # gpt-5-mini-2025-08-07

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
youtube_tool = YoutubeChannelSearchTool()

researcher = Agent(
    role="Senior Researcher",
    goal="Search the web, extract and analyze information",
    backstory="""
    You produce the highest quality research possible.
    You use multiple sources of information and you always double check
    your sources to make sure they are true and up to date.
    You want impress your coworkers with your work.
    """,
    allow_delegation=False,
    tools=[
        search_tool,
        scrape_tool,
        youtube_tool,
    ],
    max_iter=10,
    verbose=True,
)

marketer = Agent(
    role="Senior Marketer",
    goal="Come up with ideas that generate viral and useful content.",
    backstory="""
    You work at a marketing agency.
    You are the best at coming up with ideas to make content go viral.
    Your ideas are used for video, advertising, social media marketing, 
    the content you produce appeals to a young audience.
    """,
    verbose=True,
)

writer = Agent(
    role="Senior Writer",
    goal="Write scripts for viral Youtube videos.",
    backstory="""
    You write scripts for videos that keep people engaged and entertained.
    Your content is easy and fun to watch, it is informative and it makes
    people want to share it with their friends.
    You are working for a very important client.
    """,
    verbose=True,
)

branstorm_task = Task(
    description="Come up with 5 video ideas for a Youtube channel in the {industry} industry",
    agent=marketer,
    expected_output="""
    Your answer MUST be a list of 5 ideas for a Youtube video with
    an explanation of what the angle of the video would be.
    """,
    output_file="ideas_task.md",
    human_input=True,
)

selection_task = Task(
    description="Select a video idea that has the highest potential of going viral.",
    agent=writer,
    expected_output="""
    Your answer MUST include the idea that was selected as well as
    an explanation of why that selection was made.
    """,
    human_input=True,
    context=[
        branstorm_task
    ],
    output_file="selection_task.md",
)

research_task = Task(
    description="""
    Do all the research required to write the script of
    a medium length video about the selected idea.
    """,
    agent=researcher,
    expected_output="""
    You answer must have all the information a writer
    would need to write a Youtube script.
    """,
    async_execution=True,
    context=[
        selection_task,
    ],
    output_file="research_task.md",
)

competitors_task = Task(
    description="""
    Search for videos or articles in the {industry} industry that
    are simliar to the video idea we are working on and
    suggest ways our video can be different from theirs.
    """,
    agent=researcher,
    expected_output="""
    Your answer must have a list of suggetions writers can follow
    to make sure the video is as unique and as different
    from competitors as possible.
    """,
    async_execution=True,
    context=[
        selection_task,
    ],
    output_file="competitors_task.md",
)

inspiration_task = Task(
    description="""
    Search for videos or articles that are similar to the video idea
    we are working on but from other industries.
    """,
    agent=researcher,
    expected_output="""
    Your answer must have a list of examples of articles and
    videos that have a similar angle as the video we are making 
    but that are in different industries.
    """,
    async_execution=True,
    context=[
        selection_task,
    ],
    output_file="inspiration_task.md",
)

script_task = Task(
    description="""
    Write the script for a Youtube video for a channel
    in the {industry} industry.
    """,
    agent=writer,
    expected_output="""
    A script for a Youtube video with a title, an introduction,
    at least three sections, and an outro. Make sure to also include
    the prompt to generate a thumbnail for the video.
    """,
    context=[
        research_task,
        selection_task,
        competitors_task,
        inspiration_task
    ],
    output_file="script_task.md",
)

crew = Crew(
    agents=[
        researcher,
        writer,
        marketer,
    ],
    tasks=[
        branstorm_task,
        selection_task,
        research_task,
        inspiration_task,
        competitors_task,
        script_task,
    ],
    verbose=True,
)

result = crew.kickoff(
    inputs=dict(
        industry="Hot Sauce",
    )   
)

print(result)