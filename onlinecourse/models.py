from django.db import models
from django.conf import settings

# Modelos existentes: Course, Lesson, Instructor, Learner, Enrollment...

class Question(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    question_grade = models.IntegerField(default=10)

    def __str__(self):
        return "Question: " + self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        all_selected_answers = self.choice_set.filter(id__in=selected_ids).count()
        if all_answers == selected_correct and all_answers == all_selected_answers:
            return True
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission {self.id}"
