import re
from django import template

register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content
    hashtags = post.hashtags.all()
    
    for hashtag in hashtags:
            content = re.sub(
                        fr'{hashtag.content}\b', 
                        f'<a href="/posts/hashtags/{hashtag.pk}/">{hashtag.content}</a> ', 
                        content
                        )
    return content
