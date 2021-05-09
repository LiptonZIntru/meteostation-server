from django.shortcuts import redirect



def redirect_to_overview(request):
    return redirect('overview', id=1)