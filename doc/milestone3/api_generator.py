def generator(base_form: str) -> str:
    """Base Description Generator 
            API Pseudo Code"""

    prompt = make_prompt_gen(base_form)
    base_desc = model_gen(prompt)
    return post_proc_gen(base_desc)