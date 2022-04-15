# %%
import os
import openai


API_KEY = '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'
MDL_BASE = 'ada:ft-cis-700-31-2022-04-10-23-27-31'
MDL_REND = ''



def base_desc(item: str) -> str:
    """d"""
    
    # Make api call to GPT-3
    response = openai.Completion.create(
        model=MDL_BASE,
        prompt=f"item: {item}\n",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    result = response['choices'][0]['text'].strip()
    return result


def rend_desc(item: str) -> str:
    pass


# %%
if __name__ == '__main__':
    
    openai.api_key = API_KEY
    os.environ['OPENAI_API_KEY'] = openai.api_key
    
    print(base_desc('Knife'))
