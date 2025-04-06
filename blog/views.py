from datetime import date
from django.shortcuts import render,HttpResponseRedirect
from . models import Post
from django.views.generic import ListView,DetailView
from django.views import View
from .forms import CommentForm
from django.urls import reverse

# Helper function
# def get_date(post):
#   return post['date']

# def starting_page(request):
#   # This method do sorting of the posts using ORM queries
#   latest_post = Post.objects.all().order_by("-date")[:3]

#   # Below is the another method to do the sorting of the posts
#   # sorted_posts = sorted(all_posts,key=get_date)
#   # latest_post = sorted_posts[-3:]
#   return render(request,'blog/index.html',{
#     'posts':latest_post
#   })

# def posts(request):
#   all_posts = Post.objects.all().order_by("-date")
#   return render(request,'blog/all-posts.html',{
#     'all_posts':all_posts
#   })

# def post_detail(request,slug):
#   # indentified_post = Post.objects.get(slug=slug)
#   indentified_post = get_object_or_404(Post,slug = slug)
#   return render(request,'blog/post-details.html',{
#     'post':indentified_post,
#     'post_tags':indentified_post.tags.all()
#   })

class StartingPageView(ListView):
  template_name = "blog/index.html"
  model = Post
  ordering = ["-date"]
  context_object_name = "posts"

  def get_queryset(self):
        return Post.objects.all().order_by("-date")[:3]

class AllPostView(ListView):
  template_name = "blog/all-posts.html"
  model = Post
  ordering = ["-date"]
  context_object_name = "all_posts"

class SinglePostView(View):
  def is_stored_post(self,request,post_id):
    stored_posts = request.session.get("stored_posts")
    if stored_posts is not None:
      is_saved_for_later = post_id in stored_posts
    else:
      is_saved_for_later = False 
    return is_saved_for_later
  def get(self,request,slug):
    post = Post.objects.get(slug=slug) 
    
    context = {
      "post":post,
      "post_tags":post.tags.all(),
      "comment_form":CommentForm(),
      "comments":post.comments.all().order_by("-id"),
      "saved_for_later":self.is_stored_post(request,post.id)
    }
    return render(request,'blog/post-details.html',context)

  def post(self,request,slug):
    comment_form = CommentForm(request.POST)
    post = Post.objects.get(slug=slug)

    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.post = post
      comment.save()
      return HttpResponseRedirect(reverse('post-detail-page', kwargs={'slug': slug}))

    context = {
      "post":post,
      "post_tags":post.tags.all(),
      "comment_form":CommentForm,
      "comments":post.comments.all().order_by("-id"),
      "saved_for_later":self.is_saved_for_later(request,post.id)

    }
    return render(request,'blog/post-details.html',context)


class ReadLaterView(View):
  def get(self,request):
    stored_posts = request.session.get("stored_posts")
    context = {}
    if stored_posts is None or len(stored_posts)==0:
      context["posts"] = []
      context["has_posts"] = False
    else:
      posts = Post.objects.filter(id__in=stored_posts)
      context["posts"] = posts
      context["has_posts"] = True
    return render(request,'blog/stored_posts.html',context)

  def post(self,request):
    stored_posts = request.session.get("stored_posts")
    if stored_posts is None:
      stored_posts = []
    
    post_id = int(request.POST["post_id"])
    if post_id not in stored_posts:
      stored_posts.append(post_id) 
      request.session["stored_posts"] = stored_posts
    else:
      stored_posts.remove(post_id)
    request.session["stored_posts"] = stored_posts
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))