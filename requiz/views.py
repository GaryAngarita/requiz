from django.core.checks import messages
from django.shortcuts import redirect, render
import bcrypt
from django.contrib import messages
from .models import *



def cover(request):
    return render(request, "cover.html")

def logreg(request):
    return render(request, 'kid_register.html')

def kid_register(request):
    errors = KidUser.objects.reg_val(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/logreg')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        user = KidUser.objects.create(first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash)
        messages.success(request, "Registration successful!")
        request.session['id'] = user.id
        request.session['score'] = 0
        request.session['wrong'] = 0
        request.session['correct'] = 0
        request.session['total'] = 0
        request.session['percent'] = ''
    return redirect(f'start_lite/{user.id}')

def kid_login(request):
    if request.method == 'GET':
        return redirect('/')
    errors = KidUser.objects.log_val(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/logreg')
    else:
        user = KidUser.objects.get(email = request.POST['email'])
        request.session['id'] = user.id
        return redirect(f'start_lite/{user.id}')

def start_lite(request, user_id):
    context = {
        'user': KidUser.objects.get(id = user_id),
        'querys': Query.objects.all()
    }
    return render(request, "quizlite.html", context)

def addQuestion(request):
    if request.user.is_staff:
        if request.method == 'POST':
            question = request.POST['question']
            op1 = request.POST['op1']
            op2 = request.POST['op1']
            op3 = request.POST['op1']
            op4 = request.POST['op1']
            ans = request.POST['op1']
    pass

def adult_login(request):
    pass

def process_quiz(request):
    if request.method == 'POST':
        querys = Query.objects.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in querys:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        if percent <= 100 or percent >= 90:
            percent = 'Perfect!'
        elif percent < 90 or percent >= 80:
            percent = 'Really Well!'
        request.session['percent'] = percent
        request.session['total'] = total
        request.session['correct'] = correct
        request.session['wrong'] = wrong
        request.session['score'] = score
        return redirect('/results')
    else:
        querys = Query.objects.all()
        context = {
            'questions': querys
        }
        return render(request, 'quizlite.html', context)

def kid_results(request):
    context = {
        'user': KidUser.objects.get(id = request.session['id']),
        'score': request.session['score'],
        'time': request.POST.get('timer'),
        'correct': request.session['correct'],
        'wrong': request.session['wrong'],
        'percent': request.session['percent'],
        'total': request.session['total']
        }
    return render(request, 'results.html', context)



def logout(request):
    request.session.flush()
    return redirect('/')
