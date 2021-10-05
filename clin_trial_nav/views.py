from django.shortcuts import render
from django.template import loader
from . import clin_trial_main
import json
import time

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

    return render(request, 'index.jinja', context)



def results(request):
    context = {}
    
    # ADD FUNCTIONALITY HERE, TO GENERATE CONTEXT
    
    

    # define all variables in the body, then assign in the context
    # name = "Fabio"

    search = request.POST.get('search', None)

    if search:
        url = clin_trial_main.build_url_from_query(search)
        
        try:
            time_start = time.process_time()
            df_master = clin_trial_main.build_study_table(url)
            time_elapsed = time.process_time()-time_start
            
            # df_outcomes = clin_trial_main.build_outcome_table(df_master)

            # new code borrowed from geeks4geeks #
            
            json_records = df_master.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            # json_records_2 = df_outcomes.reset_index().to_json(orient='records')
            # outcome_data = []
            # outcome_data = json.loads(json_records_2)

            
            context['search'] = search
            context['url'] = url
            context['d'] = data
            context['time_elapsed'] = time_elapsed
            context['length'] = len(data)

            return render(request, 'results2.jinja', context)
        except:
            return render(request, 'no_results.jinja', context)
    else:
        return render(request, 'no_results.jinja', context)

# def results_outcomes(request):
#     context = {}

#     # get the whole row from the object that was clicked (check javascript function on how to do this?)
#     row_entry = request.POST.get('search', None)


#     return render(request, 'clin_trial_nav/results_outcomes.html', context)
