import logging
import google.cloud.logging

from vertexai.preview import reasoning_engines

from adk_agent_mcp_basic.agent import root_agent

logging.basicConfig(level=logging.INFO)
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()


agent_app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

session = agent_app.create_session(user_id="u_123")

for event in agent_app.stream_query(
    user_id="u_123",
    session_id=session.id,
    message="""
           list all the files in the directory /home/manjesh_2j/adk_to_agent_engine 
        """,
):
    print(event)
    # logging.info("[local test] " + event["content"]["parts"][0]["text"])
    # cloud_logging_client.flush_handlers()