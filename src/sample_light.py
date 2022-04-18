# %%
import os
import pickle

import random


# %%
with open('../data/light-environment.pkl', 'rb') as f:
    items = {k.lower().strip().replace('.', ''): v for k, v in
        pickle.load(f).get('base_form_to_objects').items()}

# %%
base_forms = list(items.keys())
random.shuffle(base_forms)

sample_forms = base_forms[:int(len(base_forms) * 0.1)]

# %%
