from openai import OpenAI


def chat_with_openai(api_key, initial_message=None):
    client = OpenAI(api_key=api_key)

    messages = []

    if initial_message:
        messages.append({"role": "user", "content": initial_message})

    while True:
        user_input = input("User: ")
        messages.append({"role": "user", "content": user_input})

        full_response = ""
        for response in client.chat.completions.create(
                # model="gpt-3.5-turbo",
                model="gpt-4",
                messages=messages,
                stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")

        print("Assistant:", full_response)
        messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    api_key = "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"
    chat_with_openai(api_key)
