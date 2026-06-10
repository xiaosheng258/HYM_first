from django.apps import AppConfig


class ContactappConfig(AppConfig):
    name = 'contactApp'

    def ready(self):
        import contactApp.signals
