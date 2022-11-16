from django.db import models
# timezone library used to get current time from system
from django.utils import timezone
# reverse library is used to respond back to a url request based on its name rather than
# the template name , more generic way
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    #  When working with multi-user projects
    #  (where multiple users can log in and publish/upload posts),
    #  we will not be using this approach
    #  i.e. linking author to an Authorization User (superuser)
    # because for this project scenario, only one person is going to come to this site and publish blogs
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    # The time when the post was created by superuser
    # based on current timezone that is available in settings.py in UTC
    # use just timezone.now instead of timezone.now() to five everytime current time instead ofdefault value each time you apply migrations
    created_date = models.DateTimeField(default=timezone.now)
    # the time when post was published on the site
    # it can be blank or null considering our scenario
    published_date = models.DateTimeField(blank=True,null=True)
    # As we can have publish date empty
    # we create a publish function
    # which we can call to get publish date based on current timezone
    # and save it in published_date
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # posts can have comments on them , create function for that as well
    # to only show approved comments by user on blog posts
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    # Once a Post is created, where should the site now take the user will be handled by below function
    # Once user click create post button on webpage,
    # it takes him to post detail page
    # based on the primary key of the post just created
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    # each comment is going to be connected to blog application's Post
    post = models.ForeignKey('blog.Post',on_delete=models.CASCADE,related_name='comments') # relative name is the name we give to an attribute so we can later refer to it by its name easily
    # author of the comment
    author = models.CharField(max_length=200)
    # text of comment
    text = models.TextField()
    # when comment is created by the author
    # use just timezone.now instead of timezone.now() to five everytime current time instead ofdefault value each time you apply migrations
    created_date = models.DateTimeField(default=timezone.now)
    # each comment has field approved_comment to only
    # show comments on posts that are approved by user
    # by default it is false
    approved_comment = models.BooleanField(default=False)
    # when user
    def approve(self):
        self.approved_comment = True
        self.save()

    # Once comment is created by any User
    # It takes him/her back to posts page
    # because comment needs to be first approved
    # so taking user back to the same post will not be a good idea
    # as his/her comment will not be visible on post untill approved
    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
