from django.db import models
from django.utils import timezone, dateformat

class mous(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        self.updated_at = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        return super(mous, self).save(*args, **kwargs)

class files(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    mou = models.ForeignKey(mous, on_delete=models.CASCADE, related_name= 'files', null=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.file_name
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        self.updated_at = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        return super(files, self).save(*args, **kwargs)