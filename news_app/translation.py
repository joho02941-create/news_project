from modeltranslation.translator import translator, TranslationOptions, register
from .models import News, Category


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

# translator.register(News, NewsTranslationOptions)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )