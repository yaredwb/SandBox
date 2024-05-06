import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

os.environ["SERPER_API_KEY"] = "2489394619c16b3f58de2ca3ab28532f0fb645a8"
os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo"

##################################################
# Assemble Agents
##################################################

search_tool = SerperDevTool()

# Create a senior researcher agent with memory and verbose mode
researcher = Agent(
    role='Senior Researcher',
    goal="Uncover groundbreaking insights in {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "Driven by curiosity, you are at the forefront of AI research in geotechnical engineering."
        "You have a deep understanding of the field and are always looking for new ways to apply AI to solve complex problems."
        "You are passionate about uncovering new insights and sharing your knowledge with the world."
    ),
    tools=[search_tool],
    allow_delegation=True
)

# Create a writer agent with custom tools and delegation capability
writer = Agent(
    role='Writer',
    goal="Create engaging content on {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a skilled writer with a passion for technology and innovation."
        "You have a talent for translating complex ideas into clear and engaging content."
        "You are excited to explore the applications of AI in geotechnical engineering and share your insights with a wide audience."
    ),
    tools=[search_tool],
    allow_delegation=False
)

##################################################
# Define Tasks
##################################################

research_task = Task(
    description=(
        "Research the latest developments in {topic}."
        "Identify key trends, challenges, and opportunities in the field."
        "Your final report should clearly articulate the key points,"
        "its market opportunities, and potential risks."
    ),
    expected_output="A comprehensive report on {topic}.",
    tools=[search_tool],
    agent=researcher
)

# Writing task with LLM configuration
write_task = Task(
    description=(
        "Write an engaging article on {topic}."
        "The article should be informative, engaging, and accessible to a general audience."
        "You should highlight the potential benefits and challenges."
    ),
    expected_output="A well-written article on {topic}.",
    tools=[search_tool],
    agent=writer,
    async_execution=False,
    output_file="ai_in_geotechnical_engineering.md"
)

##################################################
# Form the Crew
##################################################

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

##################################################
# Kick It Off
##################################################

result = crew.kickoff(inputs={"topic": "AI for landslides"})
print(result)