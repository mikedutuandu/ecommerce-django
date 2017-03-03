from allauth.account.views import LogoutView,LoginView,SignupView



class LoginCustom(LoginView):
    template_name = 'theme_lotus/accounts/login_view.html'

class SignupCustom(SignupView):
    template_name = 'theme_lotus/accounts/signup_view.html'
