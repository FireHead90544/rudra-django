from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as userlogin, logout as userlogout
from django.contrib import messages
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.paginator import Paginator
from django.db import connection
from .models import BlogPost, BlogComment, PostView, PostLike
from readtime import of_html
from time import perf_counter
from django.templatetags.static import static


# GET Client's IP Address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Create your views here.
def home(request):
    page_number = request.GET.get('page', 1)
    blog_posts = BlogPost.objects.order_by("-publish_date")
    paginator = Paginator(blog_posts, 10)
    page = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {
        "user": request.user,
        "page": page,
        "metatitle": "Blog | Rudransh Joshi",
        "metadescription": "Welcome to my blog! Explore my latest posts on technology, programming, my views, and more, and discover insightful articles that inform, entertain, and inspire. As a writer, I bring a unique perspective and voice to every post, backed by writings from the heart. Whether you're looking to stay up-to-date on the latest trends or gain new insights into the world of technology and programming, my blog has something for everyone.",
        "metaimage": static("blog/meta/blog-home.png"),
        "metakeywords": "blog, posts, articles, technology, programming, views, opinions, entertainment, inspiration, information, trends, insights, unique perspective, voice, writings from the heart, stay up-to-date, gain new insights, something for everyone",
    })

def search(request):
    query = request.GET.get('query', "bruh")
    page_number = request.GET.get('page', 1)
    start = perf_counter()
    if connection.vendor == "postgresql":
        results = BlogPost.objects.annotate(search=SearchVector('title', 'content', 'tldr', 'tags'),).filter(search=SearchQuery(query))
    else:
        results = BlogPost.objects.filter(title__icontains=query).union(BlogPost.objects.filter(content__icontains=query), BlogPost.objects.filter(tldr__icontains=query), BlogPost.objects.filter(tags__icontains=query)).order_by("-publish_date")
    time_taken = f"{round(perf_counter() - start, 3)}s"
    paginator = Paginator(results, 10)
    page = paginator.get_page(page_number)
    return render(request, 'blog/search.html', {
        "page": page,
        "query": query,
        "time_taken": time_taken,
        "metatitle": "Search | Rudransh Joshi",
        "metadescription": f"Search results for '{query}'"
    })

def tag(request, tag):
    tag = tag.replace("-", " ").title()
    page_number = request.GET.get('page', 1)
    start = perf_counter()
    results = BlogPost.objects.filter(tags__icontains=tag).order_by("-publish_date")
    time_taken = f"{round(perf_counter() - start, 3)}s"
    paginator = Paginator(results, 10)
    page = paginator.get_page(page_number)
    return render(request, 'blog/search.html', {
        "page": page,
        "tag": tag,
        "time_taken": time_taken,
        "metatitle": "Tag: {tag} | Rudransh Joshi",
        "metadescription": f"Posts marked with tag '{tag}'"
    })

def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname'].title()
        last_name = request.POST['lastname'].title()
        username = request.POST['username'].lower()
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username <b>{username}</b> already exists. Please choose a different username.', extra_tags="border-red-400")
            return redirect('BlogRegister')
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email <b>{email}</b> is already associated with another account. Please choose a different email.', extra_tags="border-red-400")
            return redirect('BlogRegister')

        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        user.save()
        messages.success(request, f'Account successfully created with username <b>{username}</b>. Please proceed to log in.', extra_tags="border-green-400")
        return redirect('BlogLogin')
    
    return render(request, 'blog/register.html', {
        "metatitle": "Register | Rudransh Joshi",
        "metadescription": "Register to create an account."
    })

def login(request):
    if request.user.is_authenticated:
        messages.success(request, f"Logged in as <b>{request.user}!</b>", extra_tags="border-green-400")
        return redirect('BlogHome')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            userlogin(request, user)
            messages.success(request, f"Logged in as <b>{request.user}!</b>", extra_tags="border-green-400")
            return redirect(request.GET.get('ref', 'BlogHome'))
        else:
            messages.error(request, f"Either the username or password is invalid or the user does not exists.", extra_tags="border-red-400")
            return redirect('BlogLogin')
        
    return render(request, 'blog/login.html', {
        "ref": request.GET.get('ref'),
        "metatitle": "Login | Rudransh Joshi",
        "metadescription": "Login to your account to add likes & comments and access your dashboard."
    })

def logout(request):
    if request.method == "POST":
        userlogout(request)
        messages.success(request, f"Successfully logged out!", extra_tags="border-green-400")
        return redirect(request.GET.get('ref', 'BlogHome'))
    
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'blog/dashboard.html')

    return redirect('BlogLogin')

def changename(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.first_name = request.POST['first_name'].title()
            request.user.last_name = request.POST['last_name'].title()
            request.user.save()
            messages.success(request, f"Name changed successfully!", extra_tags="border-green-400")
        
    return redirect('UserDashboard')

def changeusername(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username'].lower()
            password = request.POST['password']
            user = authenticate(username=request.user.username, password=password)
            if not user:
                messages.error(request, f"Incorrect password!", extra_tags="border-red-400")
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, f'Username <b>{username}</b> already exists. Please choose a different username.', extra_tags="border-red-400")
                else:
                    request.user.username = username
                    request.user.save()
                    messages.success(request, f"Username changed successfully!", extra_tags="border-green-400")

    return redirect('UserDashboard')

def changepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            user = authenticate(username=request.user.username, password=current_password)
            if not user:
                messages.error(request, f"Incorrect Password!", extra_tags="border-red-400")
            else:
                if new_password != confirm_password:
                    messages.error(request, f"Passwords do not match, please try again!", extra_tags="border-red-400")
                else:
                    request.user.set_password(new_password)
                    request.user.save()
                    messages.success(request, f"Password changed successfully!", extra_tags="border-green-400")
    
    return redirect('UserDashboard')

def blogpost(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    liked = False
    if request.user.is_authenticated:
        if PostLike.objects.filter(user=request.user, post=post).first():
            liked = True
    PostView.objects.get_or_create(ip=get_client_ip(request), post=post)
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replies_dict = {}
    for reply in replies:
        if reply.parent.sno not in replies_dict.keys():
            replies_dict[reply.parent.sno] = [reply]
        else:
            replies_dict[reply.parent.sno].append(reply)
    
    return render(request, 'blog/blogpost.html',
    {
        "user": request.user,
        "post": post,
        "liked": liked,
        "comments": comments,
        "replies": replies_dict,
        "read_time": of_html(post.content).minutes,
        "commentscount": BlogComment.objects.filter(post=post).count(),
        "metatitle": post.title,
        "metadescription": post.tldr,
        "metaimage": post.thumbnail.url,
        "metakeywords": post.tags 
    })

def post_comment(request):
    if not request.user.is_authenticated:
        return "User Not Authenticated!"

    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        slug = request.POST.get("slug")
        post = BlogPost.objects.get(slug=slug)
        parent = request.POST.get("parent")
        
        if not parent:
            comment = BlogComment(comment=comment, user=user, post=post)
            messages.success(request, "Your comment has been posted successfully.", extra_tags="border-green-400")
        else:
            parent = BlogComment.objects.filter(sno=parent).first()
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            messages.success(request, "Your reply has been posted successfully.", extra_tags="border-green-400")

        comment.save()

        return redirect(f'/blog/{post.slug}/')

def delete_comment(request):
    if not request.user.is_authenticated:
        return "User Not Authenticated!"
    
    if request.method == "POST":
        sno = request.POST.get("sno")
        comment = BlogComment.objects.filter(sno=sno).first()
        post_slug = ""
        if not comment:
            messages.error(request, "That comment/reply does not exist.", extra_tags="border-red-400")
        if request.user == comment.user:
            comment.delete()
            messages.success(request, "Successfully deleted the comment.", extra_tags="border-green-400")
            post_slug = comment.post.slug
        else:
            messages.success(request, "You can't delete that comment.", extra_tags="border-red-400")

        return redirect(f'/blog/{post_slug}')
    
def like_post(request):
    if not request.user.is_authenticated:
        return "User Not Authenticated!"
    
    if request.method == "POST":
        user = request.user
        post = BlogPost.objects.filter(slug=request.POST.get("slug")).first()
        post_slug = ""
        if not post:
            messages.error(request, "You can't like a post that does not exist.", extra_tags="border-red-400")
        else:
            like, created = PostLike.objects.get_or_create(user=user, post=post)
            if created:
                messages.success(request, "Liked the post!", extra_tags="border-green-400")
                post_slug = post.slug
            else:
                like.delete()
                messages.success(request, "Removed the like from the post!", extra_tags="border-green-400")
                post_slug = post.slug

        return redirect(f'/blog/{post_slug}')