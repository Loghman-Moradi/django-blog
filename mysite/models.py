from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django_resized import ResizedImageField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "df", 'Draft'
        PUBLISHED = "pb", 'Published'
        REJECTED = "rj", 'Rejected'

    CATEGORY_CHOICES = [
        ("هوش مصنوعی", "هوش مصنوعی"),
        ("برنامه نویسی", "برنامه نویسی"),
        ("تکنولوژی", "تکنولوژی"),
        ("سایر", "سایر"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="نویسنده")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(max_length=500, verbose_name="توضیحات")
    slug = models.SlugField(verbose_name="اسلاگ")
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="بروزرسانی")
    status = models.TextField(choices=Status, default=Status.DRAFT, verbose_name="وضعیت")
    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")
    category = models.CharField(choices=CATEGORY_CHOICES, default="سایر", verbose_name="دسته بندی")

    # objects = models.Manager()
    objects = jmodels.jManager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['publish']
        indexes = [
            models.Index(fields=['publish'])
        ]
        verbose_name_plural = "پست ها"

    def get_absolute_url(self):
        return reverse('mysite:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Ticket(models.Model):
    name = models.CharField(max_length=20, verbose_name='نام')
    last_name = models.CharField(max_length=20, verbose_name="نام خانوادگی")
    email = models.EmailField(max_length=50, verbose_name="ایمیل")
    phone = models.CharField(max_length=11, verbose_name="تلفن")
    description = models.CharField(max_length=250, verbose_name="متن")
    subject = models.CharField(max_length=250, verbose_name="موضوع")

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    fullname = models.CharField(max_length=20, verbose_name="نام و نام خانوادگی")
    budy = models.TextField(max_length=300, verbose_name="متن کامنت")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return self.fullname


def user_upload_to(instance, filename):
    username = instance.post.author.username
    return f'image/{username}/{filename}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images", verbose_name="پست")
    file_image = models.ImageField(upload_to=user_upload_to)
    title = models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description = models.CharField(max_length=250, verbose_name="متن", null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

    def __str__(self):
        return self.title if self.title else self.file_image.name

    def get_absolute_url(self):
        return reverse('mysite:post_detail', args=[self.post.id])


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account", verbose_name="اکانت")
    date_of_birth = jmodels.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.CharField(max_length=250, verbose_name="بایو")
    job = models.CharField(max_length=20, verbose_name="شغل", blank=True, null=True)
    photo = ResizedImageField(upload_to="account/image", blank=True, null=True, verbose_name="تصویر")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "اکانت"
        verbose_name_plural = "اکانت ها"

















