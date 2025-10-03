from django.contrib import admin

from .models import Question, Choice

admin.site.site_header = "Polls Admin Yaro"
admin.site.index_title = "The Best Admin Panel for BigBot"
admin.site.site_title = "Yaro's Page"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)



# Register your models here.
