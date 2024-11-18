from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.text import slugify  # For slug generation


"""
Structure:
- Subject: Top-level category containing Courses.
- YearGroup: Represents Nursery to Year 13.
- ExamBoard: Optional, applicable for certain courses.
- Course: Linked to Subject and YearGroup, with optional ExamBoard and Course Type.
- Module, Content, ItemBase: As previously defined.
"""


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class YearGroup(models.Model):
    name = models.CharField(max_length=50)  # e.g., Nursery, Reception, Year1, ..., Year13
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ExamBoard(models.Model):
    name = models.CharField(max_length=50)  # e.g., AQA, Edexcel, OCR
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.CASCADE)
    year_group = models.ForeignKey(YearGroup, related_name="courses", on_delete=models.CASCADE)
    examboard = models.ForeignKey(ExamBoard, related_name="courses", on_delete=models.CASCADE, null=True, blank=True)
    COURSE_TYPE_CHOICES = [
        ('Foundation', 'Foundation'),
        ('Higher', 'Higher'),
    ]
    course_type = models.CharField(
        max_length=20,
        choices=COURSE_TYPE_CHOICES,
        help_text="Select the course type (e.g., Foundation, Higher)",
        blank=True,
        null=True
    )
    title = models.CharField(max_length=200, blank=True)  # Auto-generated
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Auto-generated

    class Meta:
        unique_together = ('subject', 'year_group', 'examboard', 'course_type')
        ordering = []

    def save(self, *args, **kwargs):
        # Generate title from examboard, subject, year_group, and course_type
        parts = [
            self.examboard.name if self.examboard else None,
            self.subject.title,
            self.year_group.name,
            self.course_type
        ]
        parts = [part for part in parts if part]  # Remove None values
        self.title = " ".join(parts)
        # Generate slug from title
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}, {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module, related_name="contents", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ('text', 'video', 'image', 'file')}
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html', {'item': self}
        )


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    image = models.ImageField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
