from django.contrib import admin
from .models import Post,Author,Tag,Comments


class PostAdmin(admin.ModelAdmin):
  list_filter = ("author","tags","date",)
  list_display = ("title","date","author",)
  prepopulated_fields = {"slug":("title",)}

class CommentsAdmin(admin.ModelAdmin):
  list_display = ("user_name","post")

admin.site.register(Post,PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comments,CommentsAdmin)
