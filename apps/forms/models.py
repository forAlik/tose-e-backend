from django.db import models

class Forms(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    email = models.EmailField(default="info@ttoqom.ir", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name = 'فرم'
        verbose_name_plural = 'فرم‌ها'
