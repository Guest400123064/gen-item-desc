# %%
import openai

import argparse

import tqdm
import logging
from sentence_transformers import LoggingHandler

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    handlers=[LoggingHandler()]
)

KEY_BASE = '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'
KEY_REND = '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'
MDL_BASE = 'ada:ft-cis-700-31-2022-04-10-23-27-31'
MDL_REND = 'ada:ft-cis-700-14-2022-04-11-02-46-54'


def get_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "mode",
        type=str,
        help=f"""
        Select between base description generator and game renderer. Valid
            names are <generate> or <render>    
        """,
    )

    parser.add_argument(
        "input",
        type=str,
        help="""
        Input file name. The specific format depends on the model chosen.
            For base generation, the file should contain a single column of 
            various base item names (base forms), NO HEADER; for rendering, the file should contain 
            three columns with three columns <full_name>, <category>, and <base_description>.
        """,
    )

    parser.add_argument(
        "output",
        type=str,
        help="""
        Output filename, a new column with generated/rendered description will be appended 
            to the (copy of) input file.    
        """,
    )
    return parser


def base_desc(item: str) -> str:
    
    # Make api call to GPT-3
    openai.api_key = KEY_BASE
    response = openai.Completion.create(
        model=MDL_BASE,
        prompt=f"item: {item}\ndescription:",
        temperature=0.3,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response['choices'][0]['text'].strip().replace('\n', '')


def rend_desc(item: str, category: str, desc: str) -> str:
    
    prompt = f"""
    [ITEM]: {item}
    [CATEGORY]: {category}
    [BASE_DESC]: {desc}
    [DESC]:
    """
    
    # Make api call to GPT-3
    openai.api_key = KEY_REND
    response = openai.Completion.create(
        model=MDL_REND,
        prompt=prompt,
        temperature=0.7,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=['===']
    )
    return response['choices'][0]['text'].strip()

# %%
if __name__ == '__main__':
    
    parser = get_parser()
    args = parser.parse_args()
    
    mode = args.mode
    pin  = args.input
    pout = args.output

    # Register API key (models hosted on two accounts)
    func_desc = base_desc if mode == 'generate' else rend_desc
    dump = []
    
    logging.info(f'Reading input from <{pin}>')
    with open(pin, 'rt', encoding='utf8') as fin:
        for line in tqdm.tqdm(fin):
            line = line.strip().split('\t')
            
            line.append(func_desc(*line))
            dump.append('\t'.join(line) + '\n')      

    logging.info(f'Dumping generated description to <{pout}>')
    with open(pout, 'wt', encoding='utf8') as fout:
        fout.writelines(dump)
