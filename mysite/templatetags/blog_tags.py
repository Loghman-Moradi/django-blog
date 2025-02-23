from django import template
from django_jalali.templatetags.jformat import jformat
from django.db.models import Count, Max, Min
from markdown import markdown
from django.utils.safestring import mark_safe

from ..models import *
register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def time_of_last_post():
    return Post.objects.last().publish


@register.inclusion_tag('partials/latest-posts.html')
def latest_post(count=3):
    l_post = Post.published.order_by('-publish')[:count]
    context = {
        'l_post': l_post,
    }
    return context


@register.simple_tag()
def most_popular_post(count=3):
    return Post.published.annotate(count=Count('comments')).order_by('-count')[:count]


@register.filter(name="markdown")
def to_markdown(text):
    return mark_safe(markdown(text))


@register.simple_tag()
def most_study_time(count=1):
    return Post.published.annotate(most=Max("reading_time")).order_by('-most')[:count]


@register.simple_tag()
def minimum_study_time(count=1):
    return Post.published.annotate(min=Min("reading_time")).order_by('min')[:count]


bad_word_fa = ["احمق", "اسکل", "بیشعور"]


@register.filter(name="censor_word")
def censor(text):
    if text:
        for word in bad_word_fa:
            if word in text:
                text = text.replace(word, '*' * len(word))
        return text
    return text


@register.simple_tag()
def active_users(count=3):
    return User.objects.annotate(most=Count('posts')).order_by('-most').order_by()[:count]







