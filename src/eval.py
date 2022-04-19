# %%
import pickle
from typing import Tuple, List

import numpy as np

from sentence_transformers import SentenceTransformer
from bert_score import score

from nltk.translate.bleu_score import sentence_bleu
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
    
    
model_para = SentenceTransformer('paraphrase-albert-small-v2')
def score_para(golds: List[str], hypos: List[str]) -> List[float]:
    
    emb_gold = model_para.encode(golds, normalize_embeddings=True)
    emb_hypo = model_para.encode(hypos, normalize_embeddings=True)
    return (emb_gold * emb_hypo).sum(axis=1).tolist()
    

def score_bert(golds: List[str], hypos: List[str]) -> Tuple[List[float], List[float], List[float]]:
    
    p, r, f = score(golds, hypos, lang='en')
    return p.numpy().tolist(), r.numpy().tolist(), f.numpy().tolist()


def score_bleu(golds: List[str], hypos: List[str]) -> List[float]:
    
    def process(s: str) -> List[str]:
        
        lem = WordNetLemmatizer()
        stp = stopwords.words('english')
        
        ret = [w for w in wordpunct_tokenize(s.lower())]
        return [r for r in ret if r not in stp]

    return [sentence_bleu([process(g)], process(h), weights=[1.])
        for g, h in zip(golds, hypos)]


# %%
# Load pre-generated dataset
with open('../data/light_objects_sample_game_desc.pkl', 'rb') as fin:
    game_desc = pickle.load(fin)

all_items = []
for items in game_desc.values():
    all_items.extend(items)
    
golds = [i['gold_desc'] for i in all_items]
hypos = [i['hypo_desc'] for i in all_items]

# %%
# Eval scores
scr_para = score_para(golds, hypos)
scr_bert_p, scr_bert_r, scr_bert_f = score_bert(golds, hypos)
scr_bleu = score_bleu(golds, hypos)
for i, pa, p, r, f, b in zip(all_items, scr_para, scr_bert_p, scr_bert_r, scr_bert_f, scr_bleu):
    i['scr_para']   = pa
    i['scr_bert_p'] = p
    i['scr_bert_r'] = r
    i['scr_bert_f'] = f
    i['scr_bleu']   = b

# %%
