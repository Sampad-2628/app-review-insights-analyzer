from ..llm_client import LLMClient
from .. import config

def theme_reviews(reviews):
    """
    Assigns a theme to each review using the LLM client.
    """
    client = LLMClient()
    import os
    tagged_reviews = []
    
    print("Categorizing reviews into themes...")
    
    for r in reviews:
        theme = client.categorize_review(r['text'], config.THEME_LIST)
        
        tagged_review = r.copy()
        tagged_review['theme'] = theme
        tagged_reviews.append(tagged_review)
        
    # Ensure directory exists if saving (though this func just returns, usually caller saves)
    # Checking api.py usage -> api.py saves. So theming.py doesn't save directly.
    # Wait, api.py calls categorize_reviews_action -> save_tagged_reviews in api.py? 
    # Actually, let's check saving locations.
    return tagged_reviews
