from rest_framework import viewsets, generics, permissions, filters
from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Tag, Post, Comment
from .serializer import *
from django.core.paginator import Paginator
from .forms import CommentForm
from django.db.models import Q

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(published=True).select_related("category", "author").prefetch_related("tags", "comment_set")
    serializer_class = PostSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=slug, published=True)
        serializer.save(post=post, approved=False)




def index(request):
    posts = Post.objects.filter(published=True).order_by("-created_at")[:5]
    return render(request, "index.html", {"posts": posts})

def post_list(request):
    posts = Post.objects.filter(published=True).order_by("-created_at")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "post_list.html", {"page_obj": page_obj})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comment_set.filter(approved=True)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(
        request,
        "post_detail.html",
        {"post": post, "comments": comments, "form": form}
    )

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, published=True)
    return render(request, "category.html", {"category": category, "posts": posts})

def tag_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, published=True)
    return render(request, "tag.html", {"tag": tag, "posts": posts})

def search_view(request):
    query = request.GET.get("q")
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        published=True
    ) if query else []
    return render(request, "search.html", {"posts": posts, "query": query})

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        messages.success(request, "Thank you for your message! We will get back to you soon.")
        return redirect("contact")

    return render(request, "contact.html")