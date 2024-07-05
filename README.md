# Zania Agent

An AI agent that leverages the capabilities of a large language model and is capable to extracting answers based on the content of a large PDF document and post the results on Slack.

### Dependencies
1. This project requires `Poetry` that can be installed from https://python-poetry.org/docs/#installation
2. Post successful clone of the project on your local, create `.env` file in the root directory of the project and specify these enviroment variable with their repectives values -
    a. `OPENAI_API_KEY` - your openai api key
    b. `OPENAI_MODEL_NAME` - model of your prefrenece, this project has been developed using gpt-3.5-turbo-0125
    c. `SLACK_WEBHOOK_URL` - incoming webhook URL to post a message to a predefined channel, refer https://api.slack.com/messaging/webhooks#posting_with_webhooks
    d. `VECTOR_DB_PATH` - relative path where you want to store your vector DB


### How to run the project ?
1. Run `poetry update` to first install all the dependecies.
2. Run `poetry run streamlit run app.py`, where `app.py` is the entrypoint of the project. Go to `http://localhost:8501` to use the agent. By default the app runs on `Port NO - 8501`, to change this update the post number in the `.streamlit/config` file. The agent interface is developed using https://streamlit.io/

### Bugs & Fixes -
1. Currently the when the data is not found, `Data Not Available` is not being sent over slack. Need to identify the root cause.
2. The current chat window is dumb, need to add callabck and streams for better llm based responses.

### TODOs & Improvements - 
The project contains `#TODO` that indicate the improvements that can be furthur taken up. Broadly, these improvements can be broken down into two parts, Accuracy and User Experience. Below are some suggestions in the same.

##### For Accuracy, 
1. Try different approaches to optimize the results of similarity searches (Similarity score threshold, Max marginal relevance). Evaluate proper chunk size across different PDF files, as they vary in the structure and format of the data and page sizes.
2. More effective prompts for the agent, currently its just one chatprompt template. Also its better to break this down into different prompts and redirect accordingly by leveraging a prompt routing mechanism. 
3. Adding output parsing to the llm result for consistent output structure.
4. I would also give [LangGraph](https://langchain-ai.github.io/langgraph/) as try over [Langchain](https://www.langchain.com/) that I have currently used, as it seem to provide better controllability over the flow.

##### For enhacement of the user experience,
1. Add dynamic conversation responses from agent using LLM, add message callbacks for the input actions perfromed by the user. 
2. Using Slack web api over incoming webhook URL for better customisation of the message sent over channel.
3. Streamlit reruns are tricky and carets glitches, add better session state management to provide better user experience. Or would prefer to switch to https://docs.chainlit.io as it seems to be better alternative.