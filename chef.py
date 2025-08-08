import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task

load_dotenv()

os.environ["OPENAI_MODEL_NAME"] = "gpt-5-mini" # gpt-5-mini-2025-08-07

international_chef = Agent(
    role="International Chef",
    goal="Create ethnic cuisine recipies that are easy to cook at home",
    backstory="""
    You are an famous chef that specializeds in couisine from
    countries all around the world.
    You know how to cook the most traditional dishes from all cultures
    but you also know how to adapt them for people to be able to cook them at home.
    """,
    verbose=True,
    allow_delegation=False,
)
healthy_chef = Agent(
    role="Healthy Chef",
    goal="""
    Turn any recipe into a healthy vegetarian recipe
    that is easy to cook with home ingredients.
    """,
    backstory="""
    You are a chef specialized in healthy cooking.
    You can take any recipe and change the ingredients to make 
    it vegerarian friendly without loosing the escense of the dish 
    and what makes it delicous.
    """,
    verbose=True,
    allow_delegation=False,
)

normal_recipe = Task(
    description="Come up with a {dish} that serves {people} people.",
    agent=international_chef,
    expected_output="""
    Your answer MUST have three sections,
    the ingredients required with quantities,
    the preparation instructions and serving suggestions.
    """,
    output_file="normal_recipe.md",
)

healthy_recipe = Task(
    description="""
    Replace the ingredients of a recipe to make it vegetarian
    without making it less delicious, adjust if needed.
    """,
    agent=healthy_chef,
    expected_output="""
    Your answer MUST have four sections,
    the ingredients required with their quantities,
    the preparation instructions, serving suggestions
    and an explanation of the replaced ingredients.
    """,
    output_file="healthy_recipe.md",
)

crew = Crew(
    tasks=[
        normal_recipe,
        healthy_recipe,
    ],
    agents=[
        international_chef,
        healthy_chef,
    ],
    verbose=True,
)

result = crew.kickoff(
    inputs=dict(
        dish="Greek dinner",
        people="5",
    )
)
