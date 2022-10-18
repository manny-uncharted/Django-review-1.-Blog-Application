from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

"""
Creating a custom model manager to retrieve all posts that have a published status 
"""
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

# Defining a post model that would allow us to store the posts in the database
class Post(models.Model):


    """
    Adding a status field to the Post model: This field would allow us to save posts as drafts and publish them later. Allows us to manage the status of blog posts.
    """
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
        unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now) # This will be the date and time when the post was published
    created = models.DateTimeField(auto_now_add=True) # This will be the date and time when the post was created
    updated = models.DateTimeField(auto_now=True) # This will be the date and time when the post was updated
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') # This is the author of each post. A many-to-one relationship between posts and the user. The related_name allows us to specify the name of the reverse relationship from the User model back to the Post model. This is the name that we will use to access the posts of a given user.


    # Defining the default manager for the Post model
    objects = models.Manager()
    published = PublishedManager() # Our Custom manager


    """
    - Defining a default ordering for the posts
    - Adding a database index to the publish field: As this would help improve performance for queries filtering by the publish field.
    """
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    """
    - Defining the get_absolute_url() method on the Post model: This method will return the canonical URL for a post.
    """
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
            args=[self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug])

"""
A model to store comments on blog posts
"""
class Comment(models.Model):
    post = models.ForeignKey(Post,
        on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    