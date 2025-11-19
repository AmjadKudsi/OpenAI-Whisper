# Configuring Your Development Environment for OpenAI API

from openai import OpenAI


client = OpenAI()


def basic_example():
    try:
        response = client.models.list()
        print("API Request Successful!")
        for model in response:
            print(f"- {model.id}")
    except Exception as e:
        print(f"API Request Failed: {e}")


if __name__ == "__main__":
    basic_example()