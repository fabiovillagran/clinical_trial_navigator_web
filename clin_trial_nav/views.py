from django.shortcuts import render
from django.template import loader
from . import clin_trial_main
import json

# from django.templatetags.static import static
# from django.urls import reverse

# from jinja2 import Environment


# def environment(**options):
#     env = Environment(**options)
#     env.globals.update({
#         'static': static,
#         'url': reverse,
#     })
#     return env


# Create your views here.

def index(request):

    context= {
        
        # INSERT CONTEXT FROM MAIN FUNCTIONALITY HERE - maybe use context that exists within the template? figure out how to make work

    }

    return render(request, 'clin_trial_nav/index.html', context)



def results(request):
    context = {}
    
    # ADD FUNCTIONALITY HERE, TO GENERATE CONTEXT
    


    # define all variables in the body, then assign in the context
    # name = "Fabio"

    search = request.POST.get('search', None)

    url = clin_trial_main.build_url_from_query(search)
    df_master = clin_trial_main.build_study_table(url)

    
    # df_outcomes = clin_trial_main.build_outcome_table(df_master)

    # new code taken from geeks4geeks #
    json_records = df_master.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)

    # json_records_2 = df_outcomes.reset_index().to_json(orient='records')
    # outcome_data = []
    # outcome_data = json.loads(json_records_2)

    
    context['search'] = search
    context['url'] = url
    context['d'] = data
    # context['o'] = outcome_data

    return render(request, 'clin_trial_nav/results.html', context)

