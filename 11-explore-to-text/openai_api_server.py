'''
This module proposes code to call the internal API with APIs
Adapated to Open-WebUI in May 2026
'''

import sys
from openai import OpenAI

# Hack to bypass the control of the certificate or the .corp domain
# Another solution would be to point to a cert with the NHI root cert
import httpx
httpx_client = httpx.Client(http2=True, verify=False)


#---------------------------------------------------------------------- Constants
# Using the OpenAI API
KEY = "y7TvhP6cDdX39kVYC24LmW" # not used
API_BASE = "https://ai.partners.nhindustries.corp/v1/"


#---------------------------------------------------------------------- AI_Session
class AI_Session:
    #--- constructor
    def __init__(self, name):
        self.name = name
        self.client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=KEY,
            base_url=API_BASE,
            http_client=httpx_client # hack to avoid checking the SSL cert
        )
        self.models = self.client.models.list()
        print(f"Session '{self.name}'\nModels:")
        count = 0
        for mod in self.models.data:
            print(f"- Model index {count}: {mod.id}")
            count += 1
        self.model = self.models.data[0].id
        print(f"Working with {self.model}")

    #--- ask proposes a streaming mode or standard mode
    def ask(self, systemp, userp, assistp, streaming=False):
        messages = [
            {"role": "system",    "content": systemp}, # the system prompt
            {"role": "user",      "content":  userp},   # the user question
            {"role": "assistant", "content":  assistp}  # the previous conversation
        ]
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=streaming,
        )
        print("-" * 50)
        if streaming:
            response = ""
            # Iterate through the chunks and print tokens progressively
            for chunk in chat_completion:
                # Check if there is content delta in the choice
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    response += content
                    print(content, end="", flush=True)  # Print without newline, buffer immediately
            print("\n")  # Add a final newline after completion
        else:
            print(chat_completion)
            response = chat_completion.choices[0].message.content
            print("Response: " + response)
        print("-" * 50)

        return response



def clean_output(text):
    out = ""
    lines = text.split("\n")
    injson = False
    for l in lines:
        if l.contains(assistant):
            continue
        
        

    
    
#---------------------------------------------------------------------- Test
def main(args):
    session = AI_Session("Test")
    text = '''
    Technical context
Source documents are often but not always OCRized PDFs
Source documents in eGED are not easily available (only in database)
Cannot use cloud-based services, everything must fit on 1 L40S GPU

“AI” is a buzzword for machine/deep learning, specifically neural networks
It’s also mostly used nowadays for Large Languages Models (LLMs) based on the transformers neural net architecture
Transformers requires huge computing resources to run, and even more to train
LLMs have one huge weakness, context size, and one workaround for it: Retrieval Augmented Generation, aka “RAG”
Architecture
29/10/2025
EffAI Audit
    '''

    # Test on the metadata
    params1 = [ 
        "You are a helpful assistant, always answering in json format.",
        f"Return between 10 and 20 metadata associated with the following chunk of text comprised within pipes.\nThe answer should be a list of metadata formatted in json with the following convention: return a list of dictionaries; each dictionary has a 'key' attribute and a 'value' attribute only. | {text} |",
        ""
    ]
    response1 = session.ask(*params1, streaming = True)
    print(response1)

    # Test on the keywords
    params2 = [
        "You are a helpful assistant, always answering in json format.",
        f"Return between 10 and 20 keywords associated with the following chunk of text comprised within pipes. The answer should be a list of metadata formatted in json.\n| {text} |",
        ""
    ]
    #response2 = session.ask(*params2, streaming = True)
    #print(response2)
    

#---------------------------------------------------------------------- entry point
if __name__ == "__main__":
    main(sys.argv)

    
