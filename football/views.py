from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Comments,Club,League,Players,Replies,Quotes,Notification
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm,PostForm,PostModelForm,ProfileUpdateForm,ReplyPostForm,QuoteForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.core.exceptions import PermissionDenied
import random
from itertools import chain


# Create your views here.
@login_required
def home(request):
    # Random club matches
    league = League.objects.all()
    league_index = random.randint(0,4)
    random_league = league[league_index]
    clubs = random_league.club_set.all()
    values = list(range(20)) if len(clubs) > 18 else list(range(18))
    index = random.sample(values, k=2)
    team1 = clubs[index[0]]
    team2 = clubs[index[1]]
    # Match Time
    time_range = random.randint(1,100)
    # Random Possession
    team1_pos = random.randint(20,80)
    team2_pos = 100 - team1_pos
    # Random Shots
    shots1_range = random.randint(0,time_range)//3
    shots2_range = random.randint(0,time_range)//3
    # Random Shots on Target
    shots1_target = random.randint(0,shots1_range//2)
    shots2_target = random.randint(0,shots2_range//2)
    # Fouls
    foul1 = random.randint(0,time_range//5)
    foul2 = random.randint(0,time_range//5)
    # Random Yellow Cards
    yellow_cards1 = random.randint(0,foul1)
    yellow_cards2 = random.randint(0,foul2)
    # Random Red Cards
    red_cards1 = yellow_cards1//5
    red_cards2 = yellow_cards2//5
    # Passes
    passes1 = int(((team1_pos * time_range) / 100) * 8)
    passes2 = int(((team2_pos * time_range) / 100) * 8)
    # Pass Accuracy
    pass_acc1 = random.randint(75,95)
    pass_acc2 = random.randint(75,95)
    # Corners
    corner1 = shots1_target//2
    corner2 = shots2_target//2
    # Offsides
    offside1 = random.randint(0,time_range//15)
    offside2 = random.randint(0,time_range//15)
    # Goals
    goal1 = random.randint(0,shots1_target//2)
    goal2 = random.randint(0,shots2_target//2)
    # Goal scorers
    team1_scorers_list = team1.players_set.exclude(profile__icontains="keeper")
    team2_scorers_list = team2.players_set.exclude(profile__icontains="keeper")
    team1_scorers = random.choices(team1_scorers_list,k=goal1)
    team2_scorers = random.choices(team2_scorers_list,k=goal2)
    # Minute scored
    minutes_range = list(range(1,time_range))
    team1_minutes = sorted(random.sample(minutes_range,k=goal1))
    team2_minutes = sorted(random.sample(minutes_range,k=goal2))
    team1_goalscorers = [f'{team1_scorers.pop(0)} {team1_minutes.pop(0)}'+str("'") for _ in team1_scorers for _ in team1_minutes]
    if team1_scorers and team1_minutes:
        team1_goalscorers.append(f'{team1_scorers.pop(0)} {team1_minutes.pop(0)}'+str("'"))
    team2_goalscorers = [f'{team2_scorers.pop(0)} {team2_minutes.pop(0)}'+str("'") for _ in team2_scorers for _ in team2_minutes]
    if team2_scorers and team2_minutes:
        team2_goalscorers.append(f'{team2_scorers.pop(0)} {team2_minutes.pop(0)}'+str("'"))

    sports = Comments.objects.all()
    quotes = Quotes.objects.all()
    comments = sorted(chain(sports, quotes),key=lambda data: data.date, reverse=True)
    notifications_count = Notification.objects.filter(user=request.user,read=False).count()

    context = {'posts':comments,'team1':team1,'team2':team2,
    'team1_pos':team1_pos,'team2_pos':team2_pos,'shots1_range':shots1_range,
    'shots2_range':shots2_range,'shots1_target':shots1_target,'shots2_target':shots2_target,
    'yellow_cards1':yellow_cards1,'yellow_cards2':yellow_cards2,'red_cards1':red_cards1,
    'red_cards2':red_cards2,'passes1':passes1,'passes2':passes2,'time_range':time_range,
    'pass_acc1':pass_acc1,'pass_acc2':pass_acc2,'foul1':foul1,'foul2':foul2,'corner1':corner1,
    'corner2':corner2,'offside1':offside1,'offside2':offside2,'goal1':goal1,'goal2':goal2,
    'team1_goalscorers':team1_goalscorers,'team2_goalscorers':team2_goalscorers,'notifications_count':notifications_count}
    return render(request,'home.html',context)


class TeamList(LoginRequiredMixin,ListView):
	model = Club
	context_object_name = 'teams'
	template_name = 'teams.html'

@login_required
def team_details(request,pk):
	club = Club.objects.get(id=pk)
	context = {'club':club}
	return render(request,'team_details.html',context)

class PlayerList(LoginRequiredMixin,ListView):
	model = Club
	template_name = 'players_list.html'
	context_object_name = 'club_list'
	paginate_by = 10

class PlayerDetailView(DetailView):
	model = Players
	context_object_name = 'player'
	template_name = 'player_detail.html'

class LeagueList(LoginRequiredMixin,ListView):
	model = League
	context_object_name = 'leagues'
	template_name = 'leagues.html'

@login_required
def league_details(request,pk):
	league = League.objects.get(id=pk)
	context = {'league':league}
	return render(request,'league_details.html',context)

def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			email = form.cleaned_data.get('email')
			user = User.objects.create_user(username,email,password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			messages.success(request,"{} your account has been successfully created".format(first_name))
			return redirect('login')
	else:
		form = RegisterForm()
	context = {'form':form}
	return render(request,'registration/register.html',context)

@login_required
def profile(request):
	if request.method == "POST":
		user = get_object_or_404(User,id=request.user.id)
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance=user.profile)
		if p_form.is_valid():
			print(request.POST)
			p_form.save()
			messages.success(request,'Your profile has been updated successfully')
			redirect('profile')
	else:
		p_form = ProfileUpdateForm()
	context = {'profile_form':p_form}
	return render(request,'profile.html',context)

@login_required
def create_post(request):
	if request.method =="POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.cleaned_data.get('post')
			author = get_object_or_404(User,id=request.user.id)
			instance = Comments(post=post,author=author)
			instance.save()
			return redirect('home')
	else:
		form = PostForm()
	context = {'form':form}
	return render(request,'create_post.html',context)

@login_required
def edit_post(request,pk):
	post = get_object_or_404(Comments,id=pk)
	if request.method == "POST":
		form = PostModelForm(request.POST,instance=post)
		if form.is_valid():
			if request.user == post.author:
				form.save()
				return redirect('home')
			else:
				raise PermissionDenied
	else:
		form = PostModelForm(instance=post)		
	context = {'form':form}
	return render(request,'edit.html',context)

@login_required
def delete_post(request,pk):
	post = get_object_or_404(Comments,id=pk)
	if request.method == "POST":
		if request.user == post.author:
			post.delete()
			messages.success(request, 'Your post has been deleted successfully')
			return redirect('home')
		else:
			raise PermissionDenied
	else:
		context = {'post':post}
		return render(request,'delete.html',context)

@login_required
def reply_post(request,id):
	post = get_object_or_404(Comments,pk=id)
	if request.method == 'POST':
		form = ReplyPostForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['reply']
			instance = Replies(reply=text,comment=post,user=request.user)
			instance.save()
			return redirect(reverse('post-replies',args=[str(post.id)]))
	else:
		form = ReplyPostForm()
	context = {'post':post,'form':form}
	return render(request,'reply_form.html',context)

@login_required
def post_replies(request,id):
	post = Comments.objects.get(pk=id)
	post_replies = post.replies_set.all().order_by('-date')
	context = {'post':post,'post_replies':post_replies}
	return render(request,'post_replies.html',context)

@login_required
def post_reply_detail(request,id):
	reply = get_object_or_404(Replies,pk=id)
	context = {'reply':reply}
	return render(request,'post_reply_detail.html',context)

@login_required
def reply_delete(request,id):
	reply = get_object_or_404(Replies,pk=id)
	if request.method == 'POST':
		if reply.user == request.user:
			reply.delete()
			messages.success(request,'Your reply has been deleted')
			return redirect('home')
		else:
			raise PermissionDenied
	else:
		context = {'reply':reply}
	return render(request,'delete_reply.html',context)

@login_required
def quote_post(request,id):
	post = get_object_or_404(Comments,pk=id)
	if request.method == 'POST':
		form = QuoteForm(request.POST)
		if form.is_valid():
			quote = form.cleaned_data['quote']
			instance = Quotes(quote=quote,post=post,user=request.user)
			instance.save()
			return redirect('home')
	else:
		form = QuoteForm()
	context = {'post':post,'form':form}
	return render(request,'quote_form.html',context)

@login_required
def quotes_view(request,id):
	post = get_object_or_404(Comments,pk=id)
	context = {'post':post}
	return render(request,'post_quotes.html',context)

@login_required
def post_quote_detail(request,id):
	quote = get_object_or_404(Quotes,pk=id)
	context = {'quote':quote}
	return render(request,'post_quote_detail.html',context)

@login_required
def edit_quote(request,id):
	instance = Quotes.objects.get(pk=id)
	if request.method == 'POST':
		form = QuoteForm(request.POST)
		if form.is_valid():
			if instance.user == request.user:
				quote = form.cleaned_data['quote']
				instance.quote = quote
				instance.save()
				return redirect('home')
			else:
				raise PermissionDenied
	else:
		form = QuoteForm(initial={'quote':instance.quote})
	context = {'form':form,'edit':True,}
	return render(request,'quote_form.html',context)

@login_required
def delete_quote(request,id):
	quote = get_object_or_404(Quotes,pk=id)
	if request.method == 'POST':
		if quote.user == request.user:
			quote.delete()
			messages.success(request, 'Your quote has been deleted successfully')
			return redirect('home')
		else:
			raise PermissionDenied
	context = {'quote':quote}
	return render(request,'delete_quote.html',context)

@login_required
def reply_quote(request,id):
	quote = get_object_or_404(Quotes,pk=id)
	if request.method == 'POST':
		form = ReplyPostForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['reply']
			instance = Replies(reply=text,quote=quote,user=request.user)
			instance.save()
			return redirect(reverse('quote-replies',args=[str(quote.id)]))
	else:
		form = ReplyPostForm()
	context = {'form':form,'quote':quote}
	return render(request,'reply_form.html',context)

@login_required
def quote_replies(request,id):
	quote = get_object_or_404(Quotes,pk=id)
	quote_replies = quote.replies_set.all().order_by('-date')
	context = {'quote':quote,'quote_replies':quote_replies}
	return render(request,'quote_replies.html',context)

@login_required
def author_profile(request,id):
	user = get_object_or_404(User,pk=id)
	author_posts = Comments.objects.filter(author=user).order_by('-date')
	author_replies = Replies.objects.filter(user=user).order_by('-date')
	author_quotes = Quotes.objects.filter(user=user).order_by('-date')
	context = {'author':user,'author_posts':author_posts,'author_replies':author_replies,'author_quotes':author_quotes}
	return render(request,'author_profile.html',context)

@login_required
def notifications_view_new(request):
	notifications = Notification.objects.filter(user=request.user,read=False)
	for message in notifications:
		message.read = True
		message.save()
	context = {'notifications':notifications}
	return render(request,'notifications.html',context)

@login_required
def notifications_view_all(request):
	notifications = Notification.objects.filter(user=request.user).order_by('-date')
	context = {'notifications':notifications,'all':True}
	return render(request,'notifications.html',context)