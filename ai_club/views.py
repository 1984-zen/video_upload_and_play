import os
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, JsonResponse
from chunked_upload.response import Response
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from chunked_upload.constants import http_status
from chunked_upload.models import ChunkedUpload
from ai_club.models import mous, files, MyChunkedUpload
from ai_club.forms import RegisterMOUForm, SelectDateForm
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from django.urls import reverse
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.utils import timezone
from django.http.response import StreamingHttpResponse
from wsgiref.util import FileWrapper
import re
import mimetypes

class homeView(View):
    template_name = 'home.html'
    model = mous

    def get(self, request, *args, **kwargs):
        select_date = SelectDateForm()
        today = timezone.now()
        # 從 forms.py 拿到內建的日期選擇器
        context = {'select_date': select_date}
        mous = self.model.objects.all().order_by('-created_at')

        context['mous'] = []
        days = None
        for mou in mous:
            if mou.created_at:
                days = today - mou.created_at
            context['mous'].append((mou, days))

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        select_date = SelectDateForm(request.POST)
        context = {}
        try:
            if select_date.is_valid():
                mou_date = select_date.cleaned_data.get("mou_date")
                mou_id = self.model.objects.filter(mou_date=mou_date).values_list('id', flat=True)[0]
                if not mou_id:
                    create_mou = self.model.objects.create(mou_date=mou_date)
                    mou_id = create_mou.id
                context['mou_id'] = mou_id
                    
        except Exception as e:
            print(repr(e))

        return HttpResponseRedirect(reverse("upload_file_page", kwargs={"mou_id": mou_id}))

range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data

def stream_video(request, video_path):
    print("here", video_path)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(video_path)
    content_type, encoding = mimetypes.guess_type(video_path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(video_path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        print("here")
    else:
        resp = StreamingHttpResponse(FileWrapper(open(video_path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp


class mouView(View):
    template_name = 'room.html'
    model = mous

    def get(self, request, *args, **kwargs):
        mou_id = kwargs['mou_id']
        all_files_id_list = MyChunkedUpload.objects.filter(mou_id=mou_id)
        all_files_id_list = all_files_id_list.values_list('chunkedupload_ptr', flat = True)
        # icontains 的 i 就是不分大小寫
        mou_medias = ChunkedUpload.objects.filter(id__in=all_files_id_list).filter(filename__icontains='.mp4').filter(status=2).values('filename','file').order_by('-created_on')
        mou_other_files = ChunkedUpload.objects.filter(id__in=all_files_id_list).exclude(filename__icontains='.mp4').filter(status=2).values('filename','file').order_by('-created_on')
        context = {
            'mou_medias': mou_medias,
            'mou_other_files': mou_other_files
            }

        return render(request, self.template_name, context)


class mousUpdate(View):
    template_name = 'upload_files.html'
    model = mous

    def post(self, request, *args, **kwargs):
        form = RegisterMOUForm(request.POST)

        # 或是 request.POST 可以替代如下
        # form = RegisterMOUForm({'title':request.POST.get('title'), 'content':request.POST.get('content')})
        if form.errors:
            # 使用 valid 是 true 或 false 只能在status=200 的情況，ajax 才能在 success 接收到errors 這個 key 的訊息
            # return JsonResponse({'valid': 'false', 'errors': form.errors}, status=200)
            return JsonResponse({'errors': form.errors}, status=422)
        elif form.is_valid():
            # 因為這裡不是用 form 表，而是用 ajax 非同步傳遞給後端，所以不能直接用 form.save() 來儲存
            try:
                mou_id = kwargs['mou_id']
                mous = self.model.objects.get(id=mou_id)
                mous.title = request.POST.get('title')
                mous.content = request.POST.get('content')
                mous.save()

            except Exception as e:
                print(repr(e))

            return Response({'msg': f'update title and content successfully!'}, status=http_status.HTTP_200_OK)


class mousCreateView(View):
    template_name = 'upload_files.html'
    model = mous

    def get(self, request, *args, **kwargs):
        mou_id = kwargs['mou_id']
        current_title = self.model.objects.get(id=mou_id).title
        current_content = self.model.objects.get(id=mou_id).content
        form = RegisterMOUForm(initial={'title': current_title, 'content': current_content})
        context = {'form': form}
        # 找出讀書會的日期
        mou_date = mous.objects.filter(id=mou_id).values_list('mou_date', flat=True)[0]
        context['mou_date'] = mou_date
        context['mou_id'] = mou_id
        # 把上傳過的檔案名稱 pass to Template
        all_files_id_list = MyChunkedUpload.objects.filter(mou_id=mou_id)
        all_files_id_list = all_files_id_list.values_list('chunkedupload_ptr', flat = True)
        all_files_name = ChunkedUpload.objects.filter(id__in=all_files_id_list).filter(status=2).values_list('filename', flat = True).order_by('-created_on')
        context['all_files_name'] = all_files_name

        return render(request, self.template_name, context)


class mousListView(ListView):
    # model = mous
    template_name = 'ai_club/upload_files.html'
    queryset = mous.objects.all()
    # context_object_name = 'all_mous'


# 上傳中...
class MyChunkedUploadView(ChunkedUploadView):

    model = MyChunkedUpload
    field_name = 'the_file'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

# 上傳完成
class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):

    model = MyChunkedUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        # Do something with the uploaded file. E.g.:
        # * Store the uploaded file on another model:
        # SomeModel.objects.create(user=request.user, file=uploaded_file)
        # * Pass it as an argument to a function:
        # function_that_process_file(uploaded_file)

        upload_id = request.POST.get('upload_id')
        mou_id = request.POST.get('mou_id')
        # 先關閉 python 對檔案的開啟
        uploaded_file.file.close()
        # 檔案上傳完畢時，將記錄儲存在多對多的中間表 ai_club_mychunkedupload
        file_id = ChunkedUpload.objects.get(upload_id = upload_id).id
        mychunkedupload = MyChunkedUpload.objects.get(id = file_id)
        mychunkedupload.mou_id = mou_id
        mychunkedupload.save()
        pass

    def get_response_data(self, chunked_upload, request):

        return {
            'message':  ("You successfully uploaded '%s' (%s bytes)!" %
                        (chunked_upload.filename, chunked_upload.offset)),
            }
