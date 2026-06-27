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

from model_switcher import MODELS

#---------------------------------------------------------------------- AI_Session
class AI_Session:
    #--- constructor
    def __init__(self, name, modelnumber):
        '''
        modelnumber is related to MODELS in model_switcher
        '''
        self.name = name
        self.modelnumber = modelnumber
        self.client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=MODELS[modelnumber]["key"],
            base_url=MODELS[modelnumber]["api_base"],
            http_client=httpx_client # hack to avoid checking the SSL cert
        )
        print(f"Session '{self.name}'\nModels:")
        self.model = MODELS[modelnumber]["model"]
        print(f"Working with {self.model}")

    #--- ask proposes a streaming mode or standard mode
    def ask(self, systemp, userp, assistp, streaming=False, verbose=False):
        messages = [
            {"role": "system",    "content": systemp}, # the system prompt
            {"role": "user",      "content":  userp},   # the user question
            {"role": "assistant", "content":  assistp}  # the previous conversation
        ]
        chat_completion = self.client.chat.completions.create(
            messages = messages,
            model = self.model,
            stream = streaming,
            temperature = 0.1,
            top_p = 0.8,
        )
        if verbose: print("-" * 50)
        if streaming:
            response = ""
            # Iterate through the chunks and print tokens progressively
            for chunk in chat_completion:
                # Check if there is content delta in the choice
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    response += content
                    if verbose: print(content, end="", flush=True)  # Print without newline, buffer immediately
            if verbose: print("\n")  # Add a final newline after completion
        else:
            if verbose: print(chat_completion)
            response = chat_completion.choices[0].message.content
            if verbose: print("Response: " + response)
        if verbose: print("-" * 50)
        return response

    #---------- clean_output
    def clean_output(self, text, verbose=False):
        if self.modelnumber == 0:
            if verbose: print(f"Using {self.name} rules")
            out = ""
            lines = text.split("\n")
            inreasoning = False
            for l in lines:
                if "assistant" in l:
                    continue
                if "<think>" in l:
                    inreasoning = True
                    continue
                if "</think>" in l:
                    inreasoning = False
                    continue
                if inreasoning:
                    continue
                if l.strip() == "":
                    continue
                out += l
            if verbose: print(f"Output was cleaned:\n{out}")
            return out
        else:
            print(f"Warning: model {model} may not be supported")
            return text
    
    
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

    
