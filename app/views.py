"""
Definition of views.
"""
import json
from app.forms import ContactForm
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from django.core.serializers.json import DjangoJSONEncoder

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
  
    Cats = Category.objects.exclude(speciestable__id__isnull=True)
    SubCats = Subcategory.objects.exclude(speciestable__id__isnull=True)
    SubGrp = Subgroup.objects.exclude(speciestable__id__isnull=True)
    SpeciesTab = Speciestable.objects.exclude(reference__id__isnull=True)
    
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
        X = Subcategory.objects.filter(category_id = q).exclude(speciestable__id__isnull=True)

        return render(
            request,
            'tablesearch/catsearch.html',
            {            
                'sbcats':X,            
            }
        )



def subcats(request):
    sct = request.GET.get('sbct','')
    X = Subgroup.objects.filter(subcategory_id = sct).exclude(speciestable__id__isnull=True)

    return render(
        request,
        'tablesearch/subcatsearch.html',
        {            
            'sbgrps':X,            
        }
    )


def subgrp(request):
    sp = request.GET.get('sbgr','')
   
    X = Speciestable.objects.filter(subgroup_id = sp).exclude(reference__id__isnull=True)

    return render(
        request,
        'tablesearch/subgroupsearch.html',
        {            
            'specis':X,            
        }
    )

def specsearch(request):
    if request.method == 'GET':
        spe = request.GET.get('spec','')        
        X = Reference.objects.filter(parent_id = str(spe))
        X2 = X.values_list('parent__species','parent__latin').distinct()
        X3 = X.values_list('sitekey__site','sitekey__lat','sitekey__lon')
        X4 = json.dumps(list(X3), cls=DjangoJSONEncoder)
        if len(X2) == 0:
            pspec = ''
            plat = ''
        else:
            pspec = X2[0][0]
            plat = X2[0][1]

        lnou = len(X)

        


        return render(
            request,
            'tablesearch/SearchResult.html',
            {            
                'refdat':X,
                'pspec':pspec,
                'plat':plat,
                'lnou':lnou,
                'sites':X4
            }
        )