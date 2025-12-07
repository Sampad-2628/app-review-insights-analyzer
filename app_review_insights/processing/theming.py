from ..llm_client import LLMClient
from .. import config

def theme_reviews(reviews):
    """
    Assigns a theme to each review using the LLM client.
    """
    client = LLMClient()
    tagged_reviews = []
    
    print("Categorizing reviews into themes...")
    
    for r in reviews:
        theme = client.categorize_review(r['text'], config.THEME_LIST)
        
        tagged_review = r.copy()
        tagged_review['theme'] = theme
        tagged_reviews.append(tagged_review)
        
    return tagged_reviews
