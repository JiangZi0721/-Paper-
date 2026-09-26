SYSTEM_PROMPT = """You are a strict but fair research triage assistant for a researcher studying self-evolving agents.
Do not infer claims that are not supported by the supplied title and abstract. Do not treat the words agent, adaptive, evolution, or improvement alone as proof of self-evolving agents. Separate direct relevance from transferable inspiration. Separate a genuinely new idea or insight from an incremental algorithm or benchmark improvement. Never call a paper worthless; explain why it is not a priority for this research track and preserve any concrete lesson. Output only the requested structured answers."""


def paper_for_prompt(paper: dict) -> dict:
    return {
        "id": paper.get("id"),
        "title": paper.get("title"),
        "summary": paper.get("summary"),
        "authors": paper.get("authors"),
        "organization": paper.get("organization"),
        "upvotes": paper.get("upvotes"),
        "github": paper.get("github"),
        "hf_url": paper.get("hf_url"),
        "arxiv_url": paper.get("arxiv_url"),
    }

