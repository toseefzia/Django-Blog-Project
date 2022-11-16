from django.shortcuts import render,get_object_or_404,redirect
# get current time #
from django.utils import timezone
# Post and Comment Models imported to Views #
from blog.models import Post,Comment
# PostForm class imported to Views #
from blog.forms import PostForm,CommentForm
# reverse_lazy show data after it gets successful
from django.urls import reverse_lazy
# decorator library imported #
from django.contrib.auth.decorators import login_required
# decorators work with function views
# for CBV's we use mixins which are same thing but for class based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (View, TemplateView, ListView,
                                    DetailView, CreateView,
                                    UpdateView, DeleteView) # add multiple libraries to import in paranthesis


# Create your views here.
# class based view for About page
class AboutView(TemplateView):
    template_name = 'about.html'

# CBV for homapage where all posts can be seen
class PostListView(ListView):
    model = Post
    # Object-Relational Mapper (ORM),
    # It enables you to interact with your database, like you would with SQL
    # this function can be used to get desired data from your model class based on some filters
    def get_queryset(self):
        # grab those published posts from Post ModelClass object
        # which are __lte(less than or equal to) the current time
        #  order them based on published date
        # you can check the documentation on the given link
        # https://docs.djangoproject.com/en/4.1/topics/db/queries/
        # return ModelObject.objects.filter(attribute__lookuptype=value.order_by('-attribute'))
        # use just timezone.now instead of timezone.now() to five everytime current time instead ofdefault value each time you apply migrations
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
# using LoginRequiredMixin for authorization
class CreatPostView(LoginRequiredMixin,CreateView):
    # if user is not logged in, it should take them to login page
    login_url = '/login/'
    # if user is logged in, redirect them to post detail page
    redirect_field_name = 'blog/post_detail.html'
    # Use PostForm class from forms.py for creating post
    form_class = PostForm
    model = Post
# using LoginRequiredMixin for authorization
class PostUpdateView(LoginRequiredMixin,UpdateView):
    # if user is not logged in, it should take them to login page
    login_url = '/login/'
    # if user is logged in, redirect them to post detail page
    redirect_field_name = 'blog/post_detail.html'
    # Use PostForm class from forms.py for creating post
    form_class = PostForm
    model = Post
# using LoginRequiredMixin for authorization
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    # redirect back to post_list url after post gets deleted successfully
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    # if user is not logged in, it should take them to login page
    login_url = '/login/'
    # if user is logged in, redirect them to post detail page
    #redirect_field_name = 'blog/post_draft_list.html'
    context_object_name = 'post_draft_list'

    template_name = 'post_draft_list.html'
    model = Post

    def get_queryset(self):
        # filter posts from object of Post ModelClass
        # which do not have published date (means posts are not published)
        # and order them based on created date
        # you can check the documentation on the given link
        # https://docs.djangoproject.com/en/4.1/topics/db/queries/
        # return ModelObject.objects.filter(attribute__lookuptype=value.order_by('-attribute'))
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')




## -------------------------------------------------- ##
## -------------------------------------------------- ##
## ------ Views for Comment Model operations -------- ##
## -------------------------------------------------- ##
## -------------------------------------------------- ##
# decorator to authenticate only loggedin user can comment
@login_required
def post_publish(request,pk):
    # return requested post object using the provided primary key , if not found return 404 webpage
    post = get_object_or_404(Post,pk=pk)
    # publish post
    post.publish()
    # redirect user to post_detail page , which is actually the post just published using pk
    return redirect('post_detail',pk=pk)

# decorator to authenticate only loggedin user can comment
@login_required
def add_comment_to_post(request,pk):
    # return the requested post using the provided primary key, if post not found, return 404 page
    post = get_object_or_404(Post,pk=pk)
    # if request for adding comment on page
    if request.method == 'POST':
        # get data from commentform using post request
        form = CommentForm(request.POST)
        # if data valid
        if form.is_valid:
            # dont save directly the data by setting commit false
            comment = form.save(commit=False)
            # linking the post that we requested to comment post attribute
            comment.post = post
            # saving changes
            comment.save()
            # redirecting user to post_detail page of the post on which comment just being created
            return redirect('post_detail',pk=post.pk)
    else:
        # else just load the commentform page
        form = CommentForm()
    # saving data of comment and linking it with post using pk, render data to comment_form.html page with dictionary key form and value form
    return render(request,'blog/comment_form.html',{'form':form})

# decorator to authenticate only loggedin user can approve comment
@login_required
def comment_approve(request,pk):
    # return and save requested Comment using provided primaryKey
    comment = get_object_or_404(Comment,pk=pk)
    # call approve function
    comment.approve()
    # redirect to post_detail page using same primaryKey i.e. redirect user to same post on which commment approved
    return redirect('post_detail',pk=comment.post.pk)

# decorator to authenticate only loggedin user can approve comment
@login_required
def comment_remove(request,pk):
    # return and save requested Comment using provided primaryKey
    comment = get_object_or_404(Comment,pk=pk)
    # post'sprimarykey saved in variable
    # When comment deleted, pk of post will no longer be available to us
    post_pk = comment.post.pk
    comment.delete()
    # here we redirect to post_detail page and give pk using our saved variable post_pk
    return redirect('post_detail',pk=post_pk)
