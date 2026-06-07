from ollama import chat
from ollama import ChatResponse

def ask_llm(role, question):
    response: ChatResponse = chat(model='deepseek-r1', messages=[
        {
            'role': role,
            'content': question,
        },
    ])
    res = response['message']['content']
    print(ret)
    # or access fields directly from the response object
    #print(response.message.content)
    return ret

