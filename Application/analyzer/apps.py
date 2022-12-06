from django.apps import AppConfig
from pathlib import Path
import os
from .model import Model

class AnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analyzer'
    model = Model()
    model.load_models()