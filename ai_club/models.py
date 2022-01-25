from django.db import models
from django.utils import timezone, dateformat
# django-chunked-upload
from chunked_upload.models import ChunkedUpload

class mous(models.Model):
    mou_date = models.CharField(max_length=255, null=True)
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
    def update_mous_fields(self, title, content):
        '''更新 mous 表的 title 和 content'''
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        # 儲存後會更新 updated_at 的時間
        self.save()

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

# 'ChunkedUpload' class provides almost everything for you.
# if you need to tweak it little further, create a model class
# by inheriting "chunked_upload.models.AbstractChunkedUpload" class

class MyChunkedUpload(ChunkedUpload):

    mou = models.ForeignKey(
        mous, 
        on_delete=models.CASCADE, 
        related_name= 'chunked_uploads', 
        null=True
    )

    objects = models.Manager()