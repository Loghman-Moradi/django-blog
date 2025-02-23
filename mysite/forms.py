from django import forms
from .models import Post, Comment, User, Account


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )

    name = forms.CharField(max_length=20, label='نام', required=True)
    last_name = forms.CharField(max_length=20, label="نام خانوادگی", required=True)
    email = forms.EmailField(max_length=50, label="ایمیل")
    phone = forms.CharField(max_length=11, label="تلفن", required=True, widget=forms.TextInput)
    description = forms.CharField(max_length=250, label="متن", required=True, widget=forms.Textarea)
    subject = forms.ChoiceField(label="موضوع", choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise forms.ValidationError('شماره تلفن شما عددی نیست...')
        else:
            return phone


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['fullname', 'budy']


class PostForm(forms.ModelForm):
    image_1 = forms.ImageField(label='تصویر اول')
    image_2 = forms.ImageField(label='تصویر دوم')

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'reading_time']


class SearchForm(forms.Form):
    query = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label="نام کاربری", widget=forms.TextInput)
    password = forms.CharField(max_length=20, required=True, label="رمز عبور", widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label="رمز عبور")
    repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput, label="تکرار رمز عبور")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if repeat_password != password:
            raise forms.ValidationError('رمز عبور و تکرار آن باهم مطابقت ندارند')
        return cleaned_data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'job', 'photo']









