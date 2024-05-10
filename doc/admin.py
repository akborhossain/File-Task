from django.contrib import admin
from .models import *

# Define a custom admin class for the DocFile model
class DocFileAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description', 'created_by', 'created_at', 'updated_by', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')

admin.site.register(DocFile, DocFileAdmin)
