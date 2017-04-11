from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.urls import reverse, reverse_lazy
import os

# testing
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from users.models import Member

from .models import Rpg
from .forms import RpgForm, RpgManageForm

class Index(generic.ListView):
	template_name = 'rpgs/index.html'
	model = Rpg
	context_object_name = 'rpgs'

class Detail(generic.DetailView):
	template_name = 'rpgs/rpg.html'
	model = Rpg
	context_object_name = 'rpg'

@login_required
def join(request):
	rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
	rpg.members.add(request.user.member)
	return HttpResponseRedirect(reverse('rpg', kwargs={'pk':request.POST.get('id')}))

@login_required
def leave(request):
	rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
	rpg.members.remove(request.user.member)
	return HttpResponseRedirect(reverse('rpg', kwargs={'pk':request.POST.get('id')}))

@login_required
def create(request):
	return render(request, 'rpgs/create.html', {'form': RpgForm})

@login_required
def create_done(request):
	# create a new RPG from all the form's fields
	# except the middleware token
	# and am_i_gm which is used here instead
	# Probably not required? Pretty sure fields not in the model are ignored...
	args = {i : request.POST.get(i, None) for i in request.POST if i!='csrfmiddlewaretoken' and i!='am_i_gm'}

	args['creator_id'] = request.user.member.id

	# Make a form in order to validate the data
	fargs = RpgForm(args)

	if not fargs.is_valid():
		# TODO: Better error!
		return HttpResponse('Unknown error, contact webmonkey quoting rv57')
	me = Member.objects.get(id=request.user.member.id)

	ins = Rpg(**args)
	ins.save()
	if(request.POST.get('am_i_gm', None)):
		ins.game_masters.add(me)

	# send them to the page that was created
	return HttpResponseRedirect(reverse('rpg', kwargs={'pk': ins.id}) + '?status=created')

@login_required
def edit(request, pk):
	rpg = get_object_or_404(Rpg, id=pk)
	# TODO: Test permission code
	if rpg.creator.equiv_user.id != request.user.id:
		return HttpResponseForbidden()
	form = RpgForm(instance=rpg)
	context = {'form': form, 'id': pk}
	return render(request, 'rpgs/edit.html', context)


from .templatetags.rpg_tags import can_manage


@login_required
def edit_process(request, pk):
	rpg=get_object_or_404(Rpg, id=pk)
	if not can_manage(request.user.member, rpg):
		return HttpResponseForbidden()
	form = RpgForm(
		request.POST,
		instance=rpg
		)
	if(form.is_valid):
		form.save()
		return HttpResponseRedirect(reverse('rpg', kwargs={'pk':pk}))
	else:
		# TODO: Proper errors
		return HttpResponseBadRequest()

@login_required
def delete(request, pk):

	# TODO: ask user for confirmation !
	rpg = get_object_or_404(Rpg, id=pk)

	if not can_manage(request.user.member, rpg):
		return HttpResponseForbidden()

	rpg.delete()
	return HttpResponseRedirect(reverse('rpgs'))

# this is REALLY not scalable!
# ^ clarify?
# TODO
def manage(request, pk):
	rpg = get_object_or_404(Rpg, id=pk)
	form = RpgManageForm(instance=rpg)
	context = {'rpg': rpg, 'form': form}
	return render(request, 'rpgs/manage.html', context)

# ??????
def manage_process(request, pk):
	return HttpResponse()
