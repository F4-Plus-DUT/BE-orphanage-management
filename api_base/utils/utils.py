from django.db.models import Model


class BaseUtils:
    @staticmethod
    def active_instance(instance: Model):
        is_success = False
        if hasattr(instance, 'is_active'):
            try:
                instance.is_active = True
                instance.save()
                is_success = True
            except Exception as e:
                pass
        return False
