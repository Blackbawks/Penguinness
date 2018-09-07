"""
Definition of views.
"""
import json
import numpy as np  
import pandas as pd 
from app.forms import ContactForm
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
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

        xx = pspec.lower()
        xx = xx.replace(' ','_')
        xx = xx.replace("'",'_')
        photoname = 'photos/'+xx+'.jpg'

        lnou = len(X)

        return render(
            request,
            'tablesearch/SearchResult.html',
            {            
                'refdat':X,
                'photo':photoname,
                'pspec':pspec,
                'plat':plat,
                'lnou':lnou,
                'sites':X4
            }
        )


def divecompare(request):

    assert isinstance(request, HttpRequest)
    
    SpeciesTab = Speciestable.objects.exclude(reference__id__isnull=True)


    return render(
        request,
        'Dive_compare.html',
        {
            'title':'Compare dive depths',
            'message':'Comparing the dive depths of species in the database',
            'year':datetime.now().year,
            'spec':SpeciesTab,
        }
    )

def divedata(request):
    if request.method == 'GET':
        speid = request.GET.getlist('specid',[])        
        X = Reference.objects.filter(parent_id__in = speid).values_list('parent__species','depth')
        X2 = np.array(X,dtype=([('keys',object),('data',np.float32)]))
        X4 = Reference.objects.filter(parent_id__in = speid).order_by('parent__species','-max_depth').distinct('parent__species').values_list('parent__species','max_depth')
        X5 = np.array(X4,dtype=([('keys',object),('data',np.float32)]))
        X5 = pd.DataFrame(X5)


        tout = X2['data']==0
        X2['data'][tout] = np.nan
        
        X3 = pd.DataFrame(X2)

        group_means = X3.groupby('keys')['data'].apply(np.nanmean)

        group_means = group_means.to_frame()
        group_means = group_means.reset_index(level=['keys'])
        gms = pd.concat([group_means,X5['data']],axis=1)
        gms.columns = ['keys','data','max']
        gms = gms.round()
        out = gms.to_json(orient='columns')

        return HttpResponse({out})


def learnmore(request):
    assert isinstance(request, HttpRequest)
    
    SpeciesTab = Speciestable.objects.exclude(reference__id__isnull=True)


    return render(
        request,
        'Learn_more.html',
        {
            'title':'Compare dive depths',
            'message':'Comparing the dive depths of species in the database',
            'year':datetime.now().year,
            'spec':SpeciesTab,
        }
    )

def learnsearch(request):
    if request.method == 'GET':
        spe = request.GET.get('spec','')        
        X = Reference.objects.filter(parent_id = str(spe))
        X2 = X.values_list('parent__species','parent__latin').distinct()

        Y = X.order_by('-max_depth','depth').values_list('depth','max_depth')
        Y2 = np.array(Y,dtype=np.float32)
        X3 = pd.DataFrame(Y2)
        X3.columns = ['means','maxes']
        X3.means.loc[X3.means == 0] = np.nan
        mn = np.round(np.nanmean(X3.means),0)
        mx = np.max(X3.maxes)


        if len(X2) == 0:
            pspec = ''
            plat = ''
        else:
            pspec = X2[0][0]
            plat = X2[0][1]

        xx = pspec.lower()
        xx = xx.replace(' ','_')
        xx = xx.replace("'",'_')
        photoname = 'photos/'+xx+'.jpg'

        return render(
            request,
            'Information.html',
            {            
                'photo':photoname,
                'pspec':pspec,
                'plat':plat,
                'mxdive':mx,
                'mndive':mn
            }
        )
