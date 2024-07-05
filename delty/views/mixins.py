from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredMixin_


class LoginRequiredMixin(LoginRequiredMixin_):
    login_url = "/login"
