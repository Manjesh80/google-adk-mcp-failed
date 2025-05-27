import os
from dotenv import load_dotenv
import logging
import google.cloud.logging

import vertexai
from vertexai import agent_engines

logging.basicConfig(level=logging.INFO)
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

# Load environment variables and initialize Vertex AI
load_dotenv()
vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
    staging_bucket=f"gs://{os.getenv("GOOGLE_CLOUD_PROJECT")}-bucket",
)

# Filter agent engines for one matching the APP_NAME in this directory's .env file
ae_apps = agent_engines.list(filter=f'display_name="{os.getenv("APP_NAME", "Agent App")}"')
remote_app = next(ae_apps)
print("*****************")
print(remote_app.resource_name)
print("*****************")

exit(1)
# Get a session for the remote app
remote_session = remote_app.create_session(user_id="u_456")

test_message = """
    List all workspaces
"""

# Run the agent with this hard-coded input
events = remote_app.stream_query(
    user_id="u_456",
    session_id=remote_session["id"],
    message=test_message,
)

# Print responses
for event in events:
    print(event)
    # for part in event["content"]["parts"]:
    #     if 'text' in part:
    #         logging.info("[remote response] " + part["text"])

cloud_logging_client.flush_handlers()