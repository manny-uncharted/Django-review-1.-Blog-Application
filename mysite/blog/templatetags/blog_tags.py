from django import template
from ..models import Post

register = template.Library()


"""
Creating a simple tag to retrieve the total posts that have been published on the blog.
"""
@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}