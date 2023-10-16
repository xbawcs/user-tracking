from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, JsonResponse, QueryDict
from django import template


@login_required()
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('pages/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('pages/page-500.html')
        return HttpResponse(html_template.render(context, request))

