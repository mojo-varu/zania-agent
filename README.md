Zania Agent

An AI agent that leverages the capabilities of a large language model and is capable to extracting answers based on the content of a large PDF document and post the results on Slack.

Dependencies
1. This project requires `Poetry` that can be installed from https://python-poetry.org/docs/#installation
2. Post successful clone of the project on your local, create `.env` file in the root directory of the project and specify these enviroment variable with their repectives values -
    a. `OPENAI_API_KEY` - your openai api key
    b. `OPENAI_MODEL_NAME` - model of your prefrenece, this project has been developed using gpt-3.5-turbo-0125
    c. `SLACK_WEBHOOK_URL` - incoming webhook URL to post a message to a predefined channel, refer https://api.slack.com/messaging/webhooks#posting_with_webhooks
    d. `VECTOR_DB_PATH` - relative path where you want to store your vector DB


How to run the project ?
1. Run `poetry update` to first install all the dependecies.
2. Run `poetry run streamlit run app.py`, where `app.py` is the entrypoint of the project. Go to `http://localhost:8501` to use the agent. By default the app runs on `Port NO - 8501`, to change this update the post number in the `.streamlit/config` file. The agent interface is developed using https://streamlit.io/

Fixes -
1. Currently the Data Not Available is not being sent to slack

TODOs & Improvements - 

The project contains `#TODO` that indicate the improvements that can be furthur taken up. Broadly, these improvements can be broken down into two parts, Accuracy and User Experience. Below are some suggestions in the same.
For Accuracy, 
1. Try different approaches of similarity search or better do query decomposition. Evaluation on proper chunk size given different structure of data across PDF files.
2. More effective prompt for the agent, currently its just one chat prompt, break it down on responsibilty and add a prompt routing mechanism. 
3. Adding output parsing to the llm result for consistent structure.

For enhacement of the user experience,
1. Imporve conversation responses from agent by providing callbacks for the input actions perfromed by the user. 
2. Using Slack web api over incoming webhook for better customisation of the message sent over channel.
3. Streamlit reruns are tricky, better session state management to provide better experience.
