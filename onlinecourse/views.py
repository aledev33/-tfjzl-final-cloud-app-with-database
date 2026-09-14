from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Submission, Choice, Question


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = []
    for key, value in request.POST.items():
        if key.startswith('choice'):
            selected_choices.append(int(value))

    submission.choices.set(Choice.objects.filter(id__in=selected_choices))
    submission.save()

    return redirect('onlinecourse:show_exam_result',
                     course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choice_ids = submission.choices.values_list('id', flat=True)

    total_score = 0
    questions = Question.objects.filter(lesson__course=course)

    for question in questions:
        if question.is_get_score(selected_choice_ids):
            total_score += question.question_grade

    context = {
        'course': course,
        'grade': total_score,
        'choices': Choice.objects.filter(id__in=selected_choice_ids),
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
