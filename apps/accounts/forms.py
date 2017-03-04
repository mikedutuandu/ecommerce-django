from django import forms
from django.contrib.auth import get_user_model

from apps.accounts.models import UserAddress

User = get_user_model()


class UserAddressForm(forms.ModelForm):
    fullname = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input'}),
                               label='Họ tên')
    phone = forms.IntegerField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input'}),
                               label='Điện thoại di động')
    city = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input'}),
                           label='Tỉnh/Thành phố')
    district = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input'}),
                               label='Quận/Huyện')
    wards = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input'}),
                            label='Phường/Xã')
    street = forms.CharField(required=True,
                             widget=forms.Textarea(
                                 attrs={'class': 'form-control unicase-form-control text-input', 'rows': '2'}),
                             label='Địa chỉ')

    class Meta:
        model = UserAddress
        fields = [
            'fullname',
            'phone',
            'city',
            'district',
            'wards',
            'street',
        ]

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control unicase-form-control text-input'}),
                               label='Username')
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'form-control unicase-form-control text-input'}),label='Email address')
    old_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'class': 'form-control unicase-form-control text-input'}),label='Mật khẩu hiện tại')
    new_password1 = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'class': 'form-control unicase-form-control text-input'}),label='Mật khẩu mới')
    new_password2 = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'class': 'form-control unicase-form-control text-input'}),label='Nhập lại mật khẩu mới')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'old_password',
            'new_password1',
            'new_password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email).exclude(email=self.instance.email)
        if email_qs.exists():
            raise forms.ValidationError("Email này đã tồn tại.")
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username).exclude(username=self.instance.username)
        if username_qs.exists():
            raise forms.ValidationError("Username này đã tồn tại.")
        return username

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if old_password:
            if not self.instance.check_password(old_password):
                raise forms.ValidationError("Mật khẩu không đúng.")
        return old_password
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Xác nhận mật khẩu không đúng")
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        if password:
            self.instance.set_password(password)
        if commit:
            self.instance.save()
        return self.instance
