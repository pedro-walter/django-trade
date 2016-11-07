from django.shortcuts import render
from django.views.generic import View, TemplateView

class IndexView(View):
    def get_context(self):
        return {}    
    
    def get(self, request):
        return render(request, 'base.html', self.get_context())
        
    #def post(self, request):
    #    context = self.get_context()
        
class RegisterView(TemplateView):
    template_name = "registration/register.html"        