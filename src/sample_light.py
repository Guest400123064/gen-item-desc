# %%
import pickle
from collections import defaultdict

from gen_desc import rend_desc


with open('../data/light_objects_sample_base_desc.pkl', 'rb') as f:
    base_descriptions = pickle.load(f)


with open('../data/light-environment.pkl', 'rb') as f:
    ENVS = pickle.load(f)
    items = {k.lower().strip().replace('.', ''): v for k, v in
        ENVS.get('base_form_to_objects').items()}


def room2cat(room_id: int) -> str:
    return ENVS['rooms'][room_id]['category']


# %%
rend_descriptions = defaultdict(list)
for base_form in base_descriptions.keys():
    for obj in items[base_form]:
        in_room_ids = obj['in_room_ids']
        full_name   = obj['name']
        category    = room2cat(in_room_ids[0]) if in_room_ids else 'NULL'
        description = base_descriptions[base_form]

        print(f'base: {base_form}; obj: {full_name}')
        obj = {
            'base_form': base_form,
            'full_name': full_name,
            'category':  category,
            'base_desc': description,
            'gold_desc': ' '.join(obj['descriptions']),
            'hypo_desc': rend_desc(full_name, category, description)
        }
        
        cnt = 0
        while obj['hypo_desc'] == '' and cnt < 3:
            obj['hypo_desc'] = rend_desc(
                obj['full_name'], 
                obj['category'], 
                obj['base_desc']
            )
            cnt += 1
        
        rend_descriptions[base_form].append(obj)

# %%
for base_form, objs in rend_descriptions.items():
    for obj in objs:
        
        if obj['hypo_desc'] == '':
            print(obj['full_name'])

# %%
