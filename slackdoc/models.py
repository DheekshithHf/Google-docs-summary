from django.db import models

class SlackSummary(models.Model):
    doc_url = models.URLField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doc_url
