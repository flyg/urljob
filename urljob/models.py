from django.db import models

def enum(**enums):
    return type('Enum', (), enums)

UrlJobStatus = enum(Idle=0, Scheduling=1, Running=2)

class UrlJob(models.Model):
    url = models.CharField(max_length=1024)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    interval_minutes = models.PositiveSmallIntegerField()
    status = models.PositiveSmallIntegerField()
    last_delivered_time = models.DateTimeField()
    last_result_hash = models.CharField(max_length=40, unique=True, db_index=True)

    def view(self):
        return {
            'id': self.id,
            'url': self.url,
            'category': self.category,
            'sub_category': self.sub_category,
            'interval_minutes': self.interval_minutes,
            'status': self.status,
            'last_delivered_time': self.last_delivered_time,
            'last_result_hash': self.last_result_hash
            }
