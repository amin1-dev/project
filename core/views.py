from rest_framework import routers
from .api import QuizViewSet, QuestionViewSet, AnswerViewSet, ResponseViewSet, RecommendationViewSet, FeedbackViewSet


router = routers.DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'responses', ResponseViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'feedback', FeedbackViewSet)


from django.urls import path
from .pdf_utils import generate_career_report
from .models import Recommendation, Feedback
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Recommendation

def quiz_page(request):
    return render(request, 'quiz.html')

@login_required
def dashboard_page(request):
    recommendations = Recommendation.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user': request.user, 'recommendations': recommendations})

@login_required
def feedback_page(request):
    feedbacks = Feedback.objects.filter(user=request.user)
    return render(request, 'feedback.html', {'feedbacks': feedbacks})

@login_required
def download_report(request):
    try:
        recommendation = Recommendation.objects.filter(user=request.user).latest('generated_at')
    except Recommendation.DoesNotExist:
        raise Http404("No recommendation found.")
    return generate_career_report(request.user, recommendation)
