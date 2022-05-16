from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.core.paginator import Paginator
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    posts = Post.objects.filter(visible=True)
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'blog/home.html', {'posts': posts, 'page_obj':page_obj})

# PostDetail
def PostDetail(request, pk):
    post = Post.objects.get(pk=pk)
    if post.visible == True or request.user.is_superuser or post.author == request.user:
        comments= PostComment.objects.filter(post=post).order_by('timestamp').reverse()
        context={'post':post, 'comments': comments}
        return render(request, "blog/postdetail.html", context)


# Dashboard
def deshboard(request):
    if request.user.is_authenticated:
        post = Post.objects.all().order_by('published_date').reverse()
        paginator = Paginator(post, 5)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        if request.user.is_superuser:
            all_users = User.objects.values()
            users = [all_users[user]['username'] for user in range(len(all_users))]
            return render(request, 'blog/dashboard.html', {'post':post, 'page_obj':page_obj, 'user':'Admin', 'users':users})
        else:
            post = Post.objects.filter(author = request.user).order_by('published_date').reverse()
            paginator = Paginator(post, 5)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            return render(request, 'blog/dashboard.html', {'post':post, 'page_obj': page_obj, 'user':'Author'})
    return redirect('login')


# SignUp
class signup(View):
    def get(self, request):
        form = SignUp
        return render(request, 'blog/signup.html', {'form': form})
    def post(self, request):
        form = SignUp(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Registered Successfully!')
            form.save()
        return render(request, 'blog/signup.html', {'form': form})


# login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username = uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully !!')
                return HttpResponseRedirect('/dashboard/')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

# Change Password
def change_password(request):
 return render(request, 'blog/changepassword.html')



# Create Post
@method_decorator(login_required(), 'dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()
        post = Post.objects.get(pk=object.pk)
        messages.info(self.request, 'Your post is saved and sent for review. Once it is approved, it will be published.')
        return super(PostCreateView, self).form_valid(form)


# Update/ Edit Post
@method_decorator(login_required(), 'dispatch')
class PostEditView(UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url = reverse_lazy('dashboard')
    def get_queryset(self):
        qs = super(PostEditView, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=self.request.user)
        

# Post Approve
@login_required()
def ApprovePost(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        post.visible = True
        post.save()
        messages.info(request, 'Post is approved and visible in Samaritan blog page.')
        return redirect('home')
    return render(request, 'blog/postapprove.html', {'post' : post})


# Post Comments
def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        author=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(id=postSno)
        comment=PostComment(comment= comment, author=author, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")

    return redirect(f'/post/{post.id}')


# User Blogs List
def user_blogs_list(request, username):
    print(username)
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        print(e)
    posts = Post.objects.filter(author = user).order_by('published_date').reverse()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    if request.user.is_authenticated:
        return render(request, 'blog/list_userblogs.html', {'posts':posts, 'page_obj':page_obj})
    else:
        return redirect('login')


# Post Delete
@login_required
def PostDelete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user.is_superuser or post.author == request.user:
        post.delete()
        return redirect('/dashboard')


# Confirm Delete
@login_required
def CommentDelete(request, pk):
    if request.method == 'POST':
        post_id =request.POST.get('post_id')
        post= Post.objects.get(id=post_id)
        comment = PostComment.objects.get(sno = pk)
        print(comment.author)
        if comment.author == request.user or request.user.is_superuser:
            comment.delete()
        else:
            messages.warning(request, 'Author not delete other Comments')

        return redirect(f'/post/{post.id}')


