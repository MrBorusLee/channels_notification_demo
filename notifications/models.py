from django.db import models


from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync


class Application(models.Model):
    STATUSES = (
        ('n', 'new'),
        ('p', 'processing'),
        ('pr', 'processed')

    )
    status = models.CharField(max_length=10, choices=STATUSES)

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        async_to_sync(channel_layer.group_send)(
            f"app_{self.id}", {"type": "send_notification", 'message': 'app updated'})

        return result
