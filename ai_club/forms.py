from django import forms
from .models import mous

class RegisterMOUForm(forms.ModelForm):
    title =     forms.CharField(
                    required=False,
                    max_length=255,
                    label='讀書會標題 Title',
                    widget=forms.TextInput(
                        attrs={
                            "placeholder": "請輸入抬頭",
                            # 設定 class 或 id
                            "id": "mou_title_input"
                        }
                    )
                )
    content =   forms.CharField(
                    required=False,
                    label='讀書會描述 Description',
                    widget=forms.Textarea(
                        attrs={
                            "placeholder": "請輸入描述",
                            "rows": 10,
                            "cols": 120,
                            # 設定 class 或 id
                            "id": "mou_content_input",
                        }
                    )
                )

    class Meta:
        model = mous
        fields = ('title', 'content',)

    def clean_title(self):
        # cleaned_data = super(CommentForm, self).clean()
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('Title 不能太短')
        return title


class SelectDateForm(forms.ModelForm):
    mou_date =  forms.DateField(
                required=True,
                label = '請選擇讀書會日期',
                widget=forms.SelectDateWidget()
            )

    class Meta:
        model = mous
        fields = ('mou_date',)