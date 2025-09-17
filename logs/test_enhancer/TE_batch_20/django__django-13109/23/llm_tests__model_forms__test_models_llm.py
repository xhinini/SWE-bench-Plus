from django.test import TestCase
from django.core.exceptions import ValidationError
from django import forms
import datetime
from .models import Writer, Article

class ForeignKeyValidateBaseManagerTests(TestCase):

    def setUp(self):
        self.archived_writer = Writer._base_manager.create(name='Archived Writer', archived=True)
        self.visible_writer = Writer.objects.create(name='Visible Writer')

from django.test import TestCase
from django.apps import apps
from django.db import models, connection
from django.core.exceptions import ValidationError
from django.db import router
import uuid
from django.test import TestCase
from django.apps import apps
from django.db import models, connection
from django.core.exceptions import ValidationError
from django.db import router
import uuid

def register_and_create_models(app_label, article_name, fav_name, to_field=None, base_manager_name='base_objects'):
    """
    Dynamically create two models:
    - Article-like model with an 'archived' boolean, a 'title' and optionally a unique 'slug'
      The class will have a custom default manager that filters archived=False and a base manager
      referenced by base_manager_name.
    - Favorite-like model with a ForeignKey to the Article model (optionally to_field).

    Returns (ArticleModel, FavoriteModel)
    """
    ArticleClassName = f'{article_name}_{uuid.uuid4().hex}'
    FavoriteClassName = f'{fav_name}_{uuid.uuid4().hex}'

    class FilteredManager(models.Manager):

        def get_queryset(self):
            return super().get_queryset().filter(archived=False)
    attrs_article = {'__module__': 'tests.model_forms.models', 'title': models.CharField(max_length=50), 'archived': models.BooleanField(default=False), 'objects': FilteredManager(), base_manager_name: models.Manager()}
    if to_field:
        attrs_article['slug'] = models.CharField(max_length=50, unique=True)
    MetaArticle = type('Meta', (), {'app_label': app_label, 'base_manager_name': base_manager_name})
    attrs_article['Meta'] = MetaArticle
    ArticleModel = type(ArticleClassName, (models.Model,), attrs_article)
    fk_kwargs = {}
    if to_field:
        fk_kwargs['to_field'] = to_field
    attrs_fav = {'__module__': 'tests.model_forms.models', 'article': models.ForeignKey(ArticleModel, models.CASCADE, **fk_kwargs), 'Meta': type('Meta', (), {'app_label': app_label})}
    FavoriteModel = type(FavoriteClassName, (models.Model,), attrs_fav)
    apps.register_model(app_label, ArticleModel)
    apps.register_model(app_label, FavoriteModel)
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(ArticleModel)
        schema_editor.create_model(FavoriteModel)
    return (ArticleModel, FavoriteModel)

def unregister_and_delete_models(article_model, fav_model):
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(fav_model)
        schema_editor.delete_model(article_model)
    app_label = article_model._meta.app_label
    try:
        del apps.all_models[app_label][article_model.__name__.lower()]
    except Exception:
        pass
    try:
        del apps.all_models[app_label][fav_model.__name__.lower()]
    except Exception:
        pass