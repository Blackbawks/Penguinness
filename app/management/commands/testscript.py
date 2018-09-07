from django.core.management.base import BaseCommand

from app.models import *
import numpy as np
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        #X = Reference.objects.filter(parent_id__in = ['122','297','373']).values_list('parent__species','depth')
        #X2 = np.array(X,dtype=([('keys',object),('data',np.float32)]))
        
        #X4 = Reference.objects.filter(parent_id__in = ['122','297','373']).order_by('parent__species','-max_depth').distinct('parent__species').values_list('parent__species','max_depth')
        #X5 = np.array(X4,dtype=([('keys',object),('data',np.float32)]))
        #X5 = pd.DataFrame(X5)


        #tout = X2['data']==0
        #X2['data'][tout] = np.nan
        
        #X3 = pd.DataFrame(X2)

        #group_means = X3.groupby('keys')['data'].apply(np.nanmean)
        #group_means = group_means.to_frame()
        #group_means = group_means.reset_index(level=['keys'])
        #gms = pd.concat([group_means,X5['data']],axis=1)
        #gms.columns = ['keys','data','max']
        #gms = gms.round()
        #out = gms.to_json(orient='columns')
        #print(gms)
