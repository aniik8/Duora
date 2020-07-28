from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import *
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.list import ListView
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required(login_url='login')
def homepage(request):
    question= question_data.objects.all().order_by('-id')
    paginator = Paginator(question, 5)
    page_number = request.GET.get('page')
    question = paginator.get_page(page_number)
    context = {'question':question}
    return render(request,'quoraa/qpage.html', context)


"""The question page where you can view and ask questions."""
@login_required(login_url='login')
def questionpage(request):
    questions = question_data.objects.all().order_by('-id')
    form = question_form()
    if request.method == 'POST':
        form = question_form(request.POST)
        if form.is_valid():
            questionn = form.save(commit=False)
            questionn.user = request.user
            questionn.save()
            return redirect('question')
        else:
            form = question_form()
    context = {'form':form, 'questions':questions}
    return render(request, 'quoraa/questions.html', context)

"""This function updates the question only if current user is the user that asks the question."""

@login_required(login_url='login')
def updatequestion(request, pk):
    questions = question_data.objects.get(id=pk)
    if request.user == questions.user:
        form = question_form(instance=questions)
        if request.method == 'POST':
            form = question_form(request.POST, instance=questions)
            if form.is_valid():
                form.save()
                return redirect('question')
            else:
                return HttpResponse('Invalid form ')


        context = {'form':form}
    else:
        return HttpResponse('You cannot update Some other post')

    return render(request, 'quoraa/update.html', context)


"""As the name suggest this function deletes the question only if current user is the user that ask that question and wants to delete it."""
@login_required(login_url='login')
def deletequestion(request,pk):
    item = question_data.objects.get(id=pk)
    context = {'item':item}
    if request.user == item.user:
        if request.method == 'POST':
            item.delete()
            return redirect('question')
    else:
        return HttpResponse('You cannot Delete Some other post')

    return render(request, 'quoraa/delete_question.html', context)

"""This function takes a global variable var and shows the answer. The global variable is used so that each user can like each answer to a single question.You can 
Also give the answer if you don't and if you have submitted the answer then you can delete or update your answer."""

VAR = 1
@login_required(login_url='login')
def showanswer(request, pk):
    question = question_data.objects.get(id=pk)
    answers = answer_data.objects.filter(questions_id=pk)
    answered = False
    for answer in answers:
        if request.user == answer.user:
            answered = True
            break
        else:
            answered = False
    global VAR
    liked = False
    try:
        answers_likes = answer_data.objects.get(id=VAR)
        total_like = answers_likes.total_likes()
        if answers_likes.likes.filter(id=request.user.id).exists():
            liked = True

    except answer_data.DoesNotExist :
        total_like = 0
        liked = False
    answer_number = len(answers)

    form = answer_form()
    if request.method == 'POST':
        form = answer_form(request.POST)
        if form.is_valid():
            ans = answer_data(
                questions_id=pk,
                answer=form.cleaned_data['answer']
            )
            ans.user = request.user
            ans.save()
            return redirect('question')
        else:
            form = answer_form(instance=question)
    context = {'question': question, 'answers': answers, 'number': answer_number,
               'form': form, 'total_likes':total_like, 'liked':liked, 'answered':answered}


    return render(request, 'quoraa/showanswers.html', context)
"""This function is used to calculate the likes to each answer."""

def likeview(request, pk, slug):
    global VAR
    VAR = pk
    answer = answer_data.objects.get(id=pk)
    if answer.likes.filter(id=request.user.id).exists():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return HttpResponseRedirect(reverse('showanswer', args=[str(slug)]))

"""As the name suggests this function can update your answer. If some other person tries to update your answer then he will be shown a httpresponse"""
def updateanswer(request, pk):
    answer = answer_data.objects.get(id=pk)
    if request.user == answer.user:
        form = answer_form(instance=answer)
        if request.method == 'POST':
            form = answer_form(request.POST, instance=answer)
            if form.is_valid():
                form.save()
                return redirect('question')
            else:
                return HttpResponse('Invalid form ')


        context = {'form':form}
    else:
        return HttpResponse('You cannot update other answers')

    return render(request, 'quoraa/updateanswer.html', context)

"""This will delete your answer when you hit the submit button"""
@login_required(login_url='login')
def deleteanswer(request,pk):
    item = answer_data.objects.get(id=pk)
    context = {'item':item}
    if request.user == item.user:
        if request.method == 'POST':

            item.delete()
            messages.success(request, 'Successfully deleted.')
            return redirect('question')
    else:
        return HttpResponse('You cannot Delete Some other post')
    messages.warning(request, 'Are you sure you waana delete this answer?')
    return render(request, 'quoraa/delete_answer.html', context)

"""The signup function, as the name can explain itself is used to create your account. But be sure to follow some instructions on your signup page"""
def signup(request):
    form = signupform()
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    content = {'form':form}
    return render(request,'quoraa/signup.html', content)

"""Use for login"""
def loginfn(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('homepage')

    else:
        print('error')

    return render(request,'quoraa/login.html')


@login_required(login_url='login')
def logoutt(request):
    logout(request)
    return redirect('login')

"""This is the profile page for the users. You can edit your own profile and can also see the question you've asked along with the date and the time"""
class user_profile(ListView):
    model = profile, question_data
    template_name = 'quoraa/user_profile.html'
    context_object_name = 'user_profile_'

    def get_queryset(self):
        user_ = get_object_or_404(User, username=self.kwargs.get('username'))
        return profile.objects.filter(user=user_)

    def get_context_data(self, *, object_list=None, **kwargs):
        user_ = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super(user_profile, self).get_context_data(**kwargs)
        context['questions'] = question_data.objects.filter(user=user_)
        return context

"""This function is used to edit the profile of the current user"""
def edit_user_info(request):
    if request.method == 'POST':
        user_form = EditUserinfo(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = EditUserinfo(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form':profile_form}
    return render(request, 'quoraa/edit_user.html', context)


"""This page is only used to review your profile page after you edit your profile"""
def profile_page(request):
    return render(request, 'quoraa/profilepage.html')