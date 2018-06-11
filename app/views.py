"""
Definition of views.
"""
from app.forms import ContactForm
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template

from app.models import Countrytable, Category, Subcategory, Subgroup, Reference, Sitetable, Speciestable, PenguinnessPhotos

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def links(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'links.html',
        {
            'title':'useful links',
            'year':datetime.now().year,
        }
    )


# add to your views
def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['blackbawks.datascience@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('emailsuccess')

    return render(request, 'contact.html', {
        'form': form_class,
    })


def emailsuccess(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'emailsuccess.html',        
    )


def team(request):
    """Renders the about the team page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'Team.html',
        {
            'title':'The Team',
            'message':'The Penguinness team',
            'year':datetime.now().year,
        }
    )


def thebook(request):
    """Renders the penguiness page."""
    assert isinstance(request, HttpRequest)
  
    Cats = Category.objects.all()
    SubCats = Subcategory.objects.all()
    SubGrp = Subgroup.objects.all()
    SpeciesTab = Speciestable.objects.all()
    
    return render(
        request,
        'thebook.html',
        {
            'title':'The Book',
            'message':'The Penguinness book of records',
            'year':datetime.now().year,
            'cats':Cats,
            'sbCat':SubCats,
            'sbGrp':SubGrp,
            'spec':SpeciesTab,
        }
    )


def cats(request):
    if request.method == 'GET':
        q = request.GET.get('ct','')
        X = Subcategory.objects.filter(category_id = q)

        return render(
            request,
            'tablesearch/catsearch.html',
            {            
                'sbcats':X,            
            }
        )



def subcats(request):
    sct = request.GET.get('sbct','')
    X = Subgroup.objects.filter(subcategory_id = sct)

    return render(
        request,
        'tablesearch/subcatsearch.html',
        {            
            'sbgrps':X,            
        }
    )


def subgrp(request):
    sp = request.GET.get('sbgr','')
    X = Speciestable.objects.filter(subgroup_id = sp)

    return render(
        request,
        'tablesearch/subgroupsearch.html',
        {            
            'specis':X,            
        }
    )