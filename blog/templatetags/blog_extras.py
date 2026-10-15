from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter(name='reading_badge')
def reading_badge(post):
    """
    Format estimated reading time as a badge string.
    Example: {{ post|reading_badge }} -> "3 min read"
    """
    if hasattr(post, 'reading_time'):
        minutes = post.reading_time
    elif isinstance(post, (int, float)):
        minutes = int(post)
    else:
        words = len(str(post).split()) if post else 0
        minutes = max(1, round(words / 200))

    unit = "min" if minutes == 1 else "mins"
    return f"{minutes} {unit} read"


@register.filter(name='strip_tags_summary')
def strip_tags_summary(html_content, word_limit=30):
    """
    Strip HTML tags and truncate cleanly to word_limit words.
    """
    if not html_content:
        return ""
    clean = re.sub(r'<[^>]+>', '', html_content)
    words = clean.split()
    if len(words) <= word_limit:
        return " ".join(words)
    return " ".join(words[:word_limit]) + "..."
