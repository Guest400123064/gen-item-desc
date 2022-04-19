def renderer(setting: str, 
             full_name: str, 
             base_desc: str) -> str:
    """Renderer API Pseudo Code"""

    prompt = make_prompt_ren(setting, full_name, base_desc)
    game_desc = model_ren(prompt)
    return post_proc_ren(game_desc)