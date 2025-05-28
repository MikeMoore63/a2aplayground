from agent_executor import HelloWorldAgentExecutor

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore  # For task state management
from a2a.types import AgentCapabilities, AgentCard, AgentSkill


if __name__ == "__main__":
    # 1. Define the skill
    skill = AgentSkill(
        id="hello_world",
        name="Returns hello world",
        description="just returns hello world",
        tags=["hello world"],
        examples=["hi", "hello world"],
    )

    # 2. Define the agent card
    agent_card = AgentCard(
        name="Hello World Agent",
        description="Just a hello world agent",
        url="http://localhost:9999/",
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    # 3. Define the request handler
    request_handler = DefaultRequestHandler(
        agent_executor=HelloWorldAgentExecutor(),
        task_store=InMemoryTaskStore(),  # For task state management
    )

    # 4. Build the server
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    # 5. Start the server with Uvicorn
    import uvicorn

    uvicorn.run(server.build(), host="0.0.0.0", port=9999)
