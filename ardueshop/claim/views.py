from django.shortcuts import render, redirect
from .forms import ReclamacionForm

# Create your views here.

def do_claim(request):
    if request.method == 'POST':
        form = ReclamacionForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.user = request.user
            claim.save()
            return redirect('/my_claims')
    else:
        form = ReclamacionForm()
    
    return render(request, 'claim/do_claim.html', {'form': form})