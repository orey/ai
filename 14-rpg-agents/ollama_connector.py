from ollama import chat
from ollama import ChatResponse

import sys
sys.path.append('.')
from tools10 import Timer, interrupt

def ask_llm(role, question):
    #response: ChatResponse = chat(model='deepseek-r1', messages=[
    print(f"\n---\nROLE: {role}")
    print(f"\n---\nQUESTION: {question}")
    interrupt()
    response: ChatResponse = chat(
        model='mistral:7b',
        messages=[
            {
                'role': role,
                'content': question,
            },
        ],
        #stream = True,
    )
    input(response)
    #res = response.message.content
    res = response['message']['content']
    print(res)
    return res

