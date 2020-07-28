from django.apps import AppConfig


class QuoraaConfig(AppConfig):
    name = 'quoraa'

    def ready(self):
        import quoraa.signals

