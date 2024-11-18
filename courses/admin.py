from django.contrib import admin
from .models import Subject, Course, Module, Content, Text, File, Image, Video, YearGroup, ExamBoard

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(YearGroup)
class YearGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(ExamBoard)
class ExamBoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'year_group', 'examboard', 'course_type', 'slug')
    list_filter = ('subject', 'year_group', 'examboard', 'course_type')
    search_fields = ('title', 'subject__title', 'year_group__name')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('module', 'content_type', 'object_id', 'order')
    list_filter = ('module', 'content_type')
    search_fields = ('module__title',)


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created', 'updated')
    search_fields = ('title', 'content')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'file', 'created', 'updated')
    search_fields = ('title',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'image', 'created', 'updated')
    search_fields = ('title',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'url', 'created', 'updated')
    search_fields = ('title', 'url')
