from django.contrib import admin

from quiz.models import Category, Difficulty, Question, QuestionOption, Quiz


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    search_fields = ('code', 'title')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title',)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'category', 'text', 'difficulty')
    search_fields = ('text', 'correct_answer')
    list_filter = ('difficulty', 'quiz', 'category')
    inlines = (QuestionOptionInline,)
