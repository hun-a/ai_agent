# AI Agent System

A multi-agent AI system built with CrewAI framework that coordinates specialized agents to perform complex tasks.

## Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Serper API key (for search functionality)

## Installation

1. Clone the repository and navigate to the project directory

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Configure environment variables by creating a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KET=your_serper_api_key_here
   ```

## Usage

Execute the multi-agent system:
```bash
uv run python main.py
```

## Architecture

The system utilizes CrewAI's agent-based architecture with:
- **Agent**: Individual AI agents with specialized roles and capabilities
- **Task**: Specific objectives assigned to agents
- **Crew**: Coordination layer managing agent collaboration

## Configuration

- Model: OpenAI o4-mini (configurable via `OPENAI_MODEL_NAME`)
- Framework: CrewAI with LangChain integration
- Package Manager: uv for dependency management