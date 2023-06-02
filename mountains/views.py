from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.gis.serializers.geojson import Serializer
from django.shortcuts import get_object_or_404
from .models import *
import json, os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ReviewCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'mountains/index.html')


class MountainListView(ListView):
    template_name = 'mountains/mountain_list.html'
    context_object_name = 'mountains'
    model = Mountain


class MountainDetailView(DetailView):
    template_name = 'mountains/mountain_detail.html'
    context_object_name = 'mountain'
    model = Mountain

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mountain = self.get_object()
        serializer = Serializer()
        courses = mountain.course_set.all()
        course_details = {}
        for course in courses:
            geojson_data = serializer.serialize(CourseDetail.objects.filter(crs_name=course), fields=('geom', 'is_waypoint', 'waypoint_name'))
            course_details[course.pk] =geojson_data
        # print(course_details)
        context = {
            'mountain': mountain,
            'courses': courses,
            'course_details': course_details
        }
        # json_data = json.dumps(course_details, indent=4, sort_keys=True, ensure_ascii=False)
        # file_path = os.path.join(settings.STATICFILES_DIRS[0], 'course_details.json')
        # with open(file_path, 'w', encoding='utf-8') as file:
        #     file.write(json_data)
        return context


@login_required
def create_review(request, pk):
    mountain = Mountain.objects.get(pk=pk)
    TAG_LIST = [
        ('풍경이 아름다운', 1),
        ('장엄한', 2),
        ('설산이 아름다운', 3),
        ('단풍이 아름다운', 4),
        ('계곡이 있는', 5),
        ('바다가 보이는', 6),
        ('사진 찍기 좋은', 7),
        ('일출 명소', 8),
        ('약수물 맛이 좋은', 9),
        ('어르신과 함께', 10),
        ('아이와 함께', 11),
        ('반려견과 함께', 12),
        ('커플 끼리', 13),
        ('경사가 낮은', 14),
        ('등산 초보', 15),
        ('위험한', 16),
        ('트래킹 수준인', 17),
        ('야생 동물 출몰', 18),
        ('화장실이 많은', 19),
        ('관리가 잘된', 20),
        ('주차가 편한', 21),
        ('관광 명소가 많은', 22),
        ('맛집 꿀맛', 23),
        ('백패킹 명소', 24),
        ('야간산행하기 좋은', 25),
        ('주말등산', 26)
    ]

    if request.method == 'POST':
        form = ReviewCreationForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.mountain = mountain
            review.user = request.user
            tags = request.POST.getlist('tags')
            review.tags = list(map(int, tags))
            review.save()
            return redirect('accounts:profile', request.user.pk)
    else:
        form = ReviewCreationForm()
    context = {
        'form': form,
        'tag_list': TAG_LIST,
        'mountain': mountain,
    }
    return render(request, 'mountains/create_review.html', context)


@login_required
def review_likes(request, pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)
    return redirect('mountains:mountain_detail', pk)