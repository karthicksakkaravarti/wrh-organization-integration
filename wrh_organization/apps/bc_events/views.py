from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from apps.cycling_org.views import global_pref
from django.shortcuts import render
from .forms import SignInForm

class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Banner'] = global_pref['site_ui__banner_image']
        context['InfoBoard'] = global_pref['site_ui__home_information_board']
        return context



class SignInView(TemplateView):
    template_name = 'auth/sign_in.html'

    @method_decorator(user_passes_test(lambda user: not user.is_authenticated, login_url='index'))
    def dispatch(self, *args, **kwargs):
        return super(SignInView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            print(form)
            return self.render_to_response({'form': form})
def sign_in(request):
    form = SignInForm(request.POST or None)
    if form.is_valid():
        # Add your authentication logic here
        pass
    return render(request, 'auth/sign_in.html', {'form': form})