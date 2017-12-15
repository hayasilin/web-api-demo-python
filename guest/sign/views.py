from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
	return render(request, "index.html")	

def login_action_simple(request):
	if request.method == 'POST':
		print("Is POST")
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		if username == 'admin' and password == 'admin123':
			response = HttpResponseRedirect('/event_manage/')
			# response.set_cookie('user', username, 3600)
			request.session['user'] = username
			return response
		else:
			return render(request, 'index.html', {'error': 'username or password error!'})
			pass
		pass
	pass

def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			request.session['user'] = username
			response = HttpResponseRedirect('/event_manage/')
			request.session['user'] = username
			return response
		else:
			return render(request, 'index.html', {'error': 'username or password error!'})

@login_required
def logout(request):
	auth.logout(request)
	response = HttpResponseRedirect('/index/')

	return response

@login_required
def event_manage(request):
	# username = request.COOKIES.get('user', '')
	event_list = Event.objects.all()
	username = request.session.get('user', '')

	return render(request, "event_manage.html", {"user":username, "events": event_list})

@login_required
def search_name(request):
	username = request.session.get('user', '')
	search_name = request.GET.get('name', "")
	event_list = Event.objects.filter(name__contains=search_name)

	return render(request, "event_manage.html", {"user": username, "events": event_list})

@login_required
def guest_manage(request):
	username = request.session.get('user', '')
	guest_list = Guest.objects.all()

	paginator = Paginator(guest_list, 2)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		# 如果页数不是整型, 取第一页.
		contacts = paginator.page(1)
	except EmptyPage:
		# 如果页数超出查询范围，取最后一页
		contacts = paginator.page(paginator.num_pages)

	return render(request, "guest_manage.html", {"user": username, "guests": contacts})

	# 嘉宾手机号的查询
@login_required
def search_phone(request):
    username = request.session.get('username', '')
    search_phone = request.GET.get("phone", "")
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)

    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username, "guests": contacts, "phone":search_phone})

@login_required
def sign_index(request, eid):
	event = get_object_or_404(Event, id=eid)

	return render(request, 'sign_index.html', {'event': event})


@login_required
def sign_index_action(request, event_id):
	event = get_object_or_404(Event, id=event_id)
	guest_list = Guest.objects.filter(event_id=event_id)
	sign_list = Guest.objects.filter(sign="1", event_id=event_id)
	guest_data = str(len(guest_list))
	sign_data = str(len(sign_list))

	phone = request.POST.get('phone', '')

	result = Guest.objects.filter(phone = phone)
	if not result:
		return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error', 'guest': guest_data, 'sign': sign_data})

	result = Guest.objects.filter(phone = phone,event_id = event_id)
	if not result:
		return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})

	result = Guest.objects.get(event_id = event_id,phone = phone)

	if result.sign:
		return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'guest':guest_data,'sign':sign_data})
	else:
		Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
		return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
			'user': result,
			'guest':guest_data,
			'sign':str(int(sign_data)+1)
			})
	





