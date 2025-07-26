from rest_framework import viewsets, status, permissions
from rest_framework.response import Response as DRFResponse
from rest_framework.decorators import action, api_view, permission_classes
from .models import Quiz, Question, Answer, Response, Recommendation, Feedback, UserProfile
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, ResponseSerializer, RecommendationSerializer, FeedbackSerializer, UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ai_model.predict import predict_career

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    role = request.data.get('role', 'student')
    if not username or not password:
        return DRFResponse({'error': 'Username and password required.'}, status=400)
    if User.objects.filter(username=username).exists():
        return DRFResponse({'error': 'Username already exists.'}, status=400)
    user = User.objects.create_user(username=username, password=password, email=email)
    UserProfile.objects.create(user=user, role=role)
    return DRFResponse({'message': 'User registered successfully.'})

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return DRFResponse({'message': 'Login successful.'})
    else:
        return DRFResponse({'error': 'Invalid credentials.'}, status=400)

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Only admin can create quizzes
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'admin':
            return DRFResponse({'error': 'Only admin can create quizzes.'}, status=403)
        return super().create(request, *args, **kwargs)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Only admin can create questions
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'admin':
            return DRFResponse({'error': 'Only admin can create questions.'}, status=403)
        return super().create(request, *args, **kwargs)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Save response
        response = super().create(request, *args, **kwargs)
        # Extract features for prediction (dummy example, adapt as needed)
        answers = request.data.get('answers_json', {})
        features = {
            'Age': answers.get('Age', 25),
            'Education': answers.get('Education', 0),
            'Skills_count': answers.get('Skills_count', 3),
            'Interests_count': answers.get('Interests_count', 2)
        }
        prediction = predict_career(features)
        # Save recommendation
        Recommendation.objects.create(
            user=request.user,
            top_careers=','.join([str(c['career']) for c in prediction['top_3']]),
            scores=','.join([str(c['score']) for c in prediction['top_3']])
        )
        return response

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
