from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


"""
- Creating a view that would allow us to display all published posts
"""
def post_list(request):
    posts = Post.published.all()
    return render(request, 
        'blog/post/list.html', 
        {'posts': posts})


"""  
- Creating a view that displays a single post
"""
def post_detail(request, id):
    try:
        post = get_object_or_404(Post, 
            id=id, 
            status=Post.Status.PUBLISHED)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request,
        'blog/post/detail.html',
        {'post': post})


