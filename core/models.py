from django.db import models
from django.contrib.auth.models import User

# User profile to extend default User with role
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# Quiz and questions
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('mcq', 'Multiple Choice'),
        ('likert', 'Likert Scale'),
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    choices = models.TextField(blank=True, help_text="Semicolon-separated choices for MCQ")

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    # Optionally, store all answers as JSON
    answers_json = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

# Feedback
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback from {self.user.username}"

# AI Recommendation per user
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    top_careers = models.TextField(help_text="Comma-separated career names")
    scores = models.TextField(help_text="Comma-separated confidence scores")
    generated_at = models.DateTimeField(auto_now_add=True)
    report_pdf = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return f"Recommendation for {self.user.username}"
