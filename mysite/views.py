from django.views.generic import View
from django.shortcuts import render_to_response


class Home(View):
    TEMPLATE = 'home.html'
    def get(self,request):
        context = {}
        return render_to_response(self.TEMPLATE,context)