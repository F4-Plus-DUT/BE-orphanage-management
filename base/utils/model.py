from django.db.models import Model

from common.constants.base import Flag


class ModelUtils:
    @staticmethod
    def active_instance(instance: Model, status: Flag = Flag.ON):
        is_success = False
        if hasattr(instance, 'is_active'):
            try:
                instance.is_active = status.value
                instance.save()
                is_success = True
            except Exception as e:
                print(e)
                is_success = False
        return is_success

    @staticmethod
    def get_model_name(instance: Model):
        return instance._meta.verbose_name
