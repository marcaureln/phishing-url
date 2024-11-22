import json
import os
import re

import pandas as pd
from dotenv import load_dotenv
from joblib import load
from openai import OpenAI

from src.build_features import extract_feature


def is_phishing(guess: bool):
    return guess


def classify_url(url: str, model: str):
    # Load the API key from the .env file
    load_dotenv()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # Create a client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    # "function definitions" for the OpenAI API. This helps the model understand what the functions are supposed to do.
    tools = [
        {
            "type": "function",
            "function": {
                "name": "is_phishing",
                "description": "Determines if this URL is a phishing website.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "guess": {
                            "type": "boolean",
                            "description": "The guess of whether the website is a phishing website.",
                        },
                    },
                    "required": ["guess"],
                    "additionalProperties": False,
                },
            },
        },
    ]

    # Prompt the model
    messages = [
        {
            "role": "system",
            "content": "You are a website security tool. You have been asked to determine if the following URL is a phishing website.",
        },
        {
            "role": "user",
            "content": f"This is the URL of the website: {url}",
        },
    ]

    # Make a request to the API
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        stream=False,  # Return all messages at once
        parallel_tool_calls=True,  # Functions can be called in parallel - no need to be executed sequentially
        tool_choice="required",  # Forces the assistant to use the tools
        temperature=0.0,  # No randomness/creativity in the responses,
    )

    for choice in response.choices:
        if choice.message.tool_calls:
            # Arguments are passed as a JSON string
            tool_call = choice.message.tool_calls[0]
            # Parse arguments as JSON
            arguments = json.loads(tool_call.function.arguments)
            # Extract the guessed value
            guess = arguments['guess']
            return guess
        if choice.message.content:
            # Some Non-OpenAI models returns tool_calls as part of the message content (as a string)
            # Extract the JSON part using regex
            content = choice.message.content
            json_str = re.search(r'\[TOOL_CALLS\] (\[.*?\])', content).group(1)
            # Parse the JSON
            tool_calls = json.loads(json_str)
            tool_call = tool_calls[0]
            # Extract the guessed value
            guess = tool_call['arguments']['guess']
            return guess


def custom_predict(model, data_frame: pd.DataFrame, legitimate_threshold=0.5, phishing_threshold=0.5):
    X = data_frame.drop(columns=["url"], axis=1)
    probs = model.predict_proba(X)[:, 1]  # Probability of being spam
    predictions = model.predict(X)

    for i in range(len(predictions)):
        if probs[i] >= phishing_threshold:
            predictions[i] = 1
        elif probs[i] <= legitimate_threshold:
            predictions[i] = 0
        else:
            try:
                prediction = classify_url(data_frame.iloc[i]["url"], model="anthropic/claude-3-5-haiku")
                predictions[i] = int(prediction)
            except Exception as e:
                print(f"Error: {e}")
                print(f"URL: {data_frame.iloc[i]['url']}")
                predictions[i] = 1  # Assume phishing if there's an error

    return probs, predictions


def predict(url: str):
    features = extract_feature(url)
    df = pd.DataFrame(features, index=[0])
    df['url'] = url

    pipeline = load('../models/random_forest_with_pipeline.joblib')

    y_proba, y_pred = custom_predict(pipeline, df, legitimate_threshold=0.2, phishing_threshold=0.8)

    print(f"Probability: {y_proba[0]}")
    print(f"Prediction: {y_pred[0]}")

    return y_pred[0]


if __name__ == "__main__":
    predict('https://www.google.com')
