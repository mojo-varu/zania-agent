Zania Agent

An AI agent that leverages the capabilities of a large language model and is capable to extracting answers based on the content of a large PDF document and post the results on Slack.

Dependencies
1. This project requires `Poetry` that can be installed from https://python-poetry.org/docs/#installation
2. Post successful clone of the project on your local, create `.env` file in the root directory of the project and specify these enviroment variable with their repectives values
    `OPENAI_API_KEY` - your openai api key
    `OPENAI_MODEL_NAME` - model of your prefrenece, this project has been developed using gpt-3.5-turbo-0125
    `SLACK_WEBHOOK_URL` - incoming webhook URL to post a message to a predefined channel, refer https://api.slack.com/messaging/webhooks#posting_with_webhooks
    `VECTOR_DB_PATH` - relative path where you want to store your vector DB


How to run the project ?
1. Run `poetry update` to first install all the dependecies.
2. Run `poetry run streamlit run app.py`, where `app.py` is the entrypoint of the project. Go to `http://localhost:8501` to use the agent.
   The agent interface is developed using https://streamlit.io/


TODOs & Improvements
The project contains `#TODO` that indicate those improvements that can be taken up. In general, these improvements can be broken down into two parts.
1. Improvement in the accuracy of the results, this requires making the RAG more effective, trying different approaches of semantic similarity search, query decomposition.
2. Enhacement of the user experience, with respect to conversations responses from the agent. Also using Slack web api over incoming webhook for better customisation of the message.
