from django.apps import AppConfig


class Quizapp2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Quizapp2'

    def ready(self) -> None:
        import Quizapp2.signals
