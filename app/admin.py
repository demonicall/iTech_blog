from django.contrib import admin
from .models import Category, Tag, Post, Comment, Contact
from ckeditor.widgets import CKEditorWidget
from django import forms

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),
        }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "author", "category", "published", "created_at")
    list_filter = ("published", "category", "tags")
    search_fields = ("title", "content")
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('featured_image', 'content')
        }),
        ('Status', {
            'fields': ('published',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "email", "approved", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("email", "body", "post__title")
    list_editable = ("approved",)
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"


from .models import Contact  # Add this import


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "read")
    list_filter = ("read", "created_at")
    search_fields = ("email", "message")
    list_editable = ("read",)
    readonly_fields = ("email", "message", "created_at")

    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        queryset.update(read=True)

    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(read=False)

    mark_as_unread.short_description = "Mark selected messages as unread"

    fieldsets = (
        ('Contact Information', {
            'fields': ('email',)
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'read')
        }),
    )