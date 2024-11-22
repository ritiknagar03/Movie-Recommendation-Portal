from django.shortcuts import render
from MRP.get_recommendations import get_recommendations


def get_movie(request):
    context = {
        'message': None,
        'recommendations': None
    }
    if request.method == 'POST':
        genre = request.POST.get('Genre')
        certificate = request.POST.get('certificate')
        rating = request.POST.get('rating')
        recommendations = get_recommendations(genre, certificate, float(rating))

        if isinstance(recommendations, str):
            context['message'] = recommendations
            context['recommendations'] = None
        else:
            context['recommendations'] = recommendations

    return render(request, 'index.html', context)


# Create your views here.
