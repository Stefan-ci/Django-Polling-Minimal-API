from django.contrib import admin
from polls.models import Poll, Answer


class InlinePollAnswer(admin.TabularInline):
    model = Answer
    #classes = ["collapse"]
    fields = ["answer", "is_active"]
    


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["poll", "answer", "is_active", "created_on"]
    list_filter = ["is_active", "created_on"]
    search_fields = ["poll", "is_active", "created_on", "poll__question", "poll__slug"]
    date_hierarchy = "created_on"
    
    # If you want to delete an answer, set its status to inactive by deactivating "is_active"
    def has_delete_permission(self, request, obj=None):
        return False




class PollAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("question",),
    }
    list_display = ["question", "is_active", "created_on", "count_active_answers"]
    list_filter = ["is_active", "created_on"]
    search_fields = ["question", "is_active", "created_on", "slug"]
    date_hierarchy = "created_on"
    inlines = [InlinePollAnswer]
    
    # If you want to delete a poll, set its status to inactive by deactivating "is_active"
    def has_delete_permission(self, request, obj=None):
        return False
    


admin.site.register(Poll, PollAdmin)    
admin.site.register(Answer, AnswerAdmin)    
