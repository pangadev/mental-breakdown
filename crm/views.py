from django.shortcuts import render
from crm.forms import *
from crm.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone
from .render import Render


# Create your views here.
class MainPage(View):
    def get(self, request):
        words = ['Bad', 'Simple', 'Stupid', 'Unknown', 'Best']
        user = request.user
        word = random.choice(words)
        return render(request, 'main_page.html', {'word': word, 'user': user})


class ContactCreate(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.fields["created_by"] = request.user
            contact = form.save(commit=False)
            contact.created_by = request.user
            now = timezone.now()
            contact.updated_at = now
            contact.save()
            form.save_m2m()
            # form.save()
            return HttpResponseRedirect(f'/contact/view/{contact.pk}')
        return render(request, 'contact.html', {'form': form})


class ContactView(View):
    def get(self, request, id):
        contact = Contact.objects.get(id=id)
        # activites = Activity.objects.filter(activity_contact=contact).order_by('-created_at')
        activities1 = Activity.objects.filter(activity_contact=contact).order_by('-updated_at')[0:1]
        activities2 = Activity.objects.filter(activity_contact=contact).order_by('-updated_at')[1:2]
        activities3 = Activity.objects.filter(activity_contact=contact).order_by('-updated_at')[2:4]
        activities4 = Activity.objects.filter(activity_contact=contact).order_by('-updated_at')[4:]
        activity_form = ActivityForm()
        # relationship_form = ContactRelationshipForm(my_arg=int(id))
        from_relationships = ContactRelationship.objects.filter(from_contact=contact)
        to_relationships = ContactRelationship.objects.filter(to_contact=contact)
        return render(request, 'contact.html',
                      {'contact': contact, 'activity_form': activity_form, 'activities1': activities1,
                       'activities2': activities2, 'activities3': activities3, 'activities4': activities4,
                       'from_relationships': from_relationships, 'to_relationships': to_relationships})

    def post(self, request, id):
        form = ActivityForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            contact = Contact.objects.get(id=id)
            now = timezone.now()
            contact.updated_at = now
            contact.save()
            activity = Activity.objects.create(title=title, description=description, activity_contact=contact)
            return HttpResponseRedirect(f'/contact/view/{id}')
        return render(request, 'contact.html', {'form': form})


class ActivityEdit(View):
    def get(self, request, id, activity_id):
        activity = Activity.objects.get(id=activity_id)
        # contact = Contact.objects.get(id=activity.activity_contact.id)
        contact = Contact.objects.get(id=id)
        activity_form = ActivityForm(
            initial={'title': activity.title, 'description': activity.description})
        from_relationships = ContactRelationship.objects.filter(from_contact=contact)
        to_relationships = ContactRelationship.objects.filter(to_contact=contact)
        return render(request, 'contact.html',
                      {'contact': contact, 'activity_form': activity_form,
                       'from_relationships': from_relationships, 'to_relationships': to_relationships})

    def post(self, request, id, activity_id):
        form = ActivityForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            contact = Contact.objects.get(id=id)
            contact.updated_at = timezone.now()
            contact.save()
            Activity.objects.filter(id=activity_id).update(title=title, description=description,
                                                           updated_at=timezone.now())
            return HttpResponseRedirect(f'/contact/view/{id}')
        return render(request, 'contact.html', {'form': form})


class ActivityDelete(View):
    def get(self, request, id, activity_id):
        activity = Activity.objects.filter(id=activity_id)
        activity.delete()
        contact = Contact.objects.get(id=id)
        contact.updated_at = timezone.now()
        contact.save()
        # contact = Contact.objects.get(id=activity.activity_contact.id)
        # contact = Contact.objects.get(id=id)
        # activity_form = ActivityForm(initial={'title': activity.title, 'description': activity.description})
        # from_relationships = ContactRelationship.objects.filter(from_contact=contact)
        # to_relationships = ContactRelationship.objects.filter(to_contact=contact)
        return HttpResponseRedirect(f'/contact/view/{id}')


class ContactEdit(View):
    def get(self, request, id):
        contact = Contact.objects.get(id=id)
        form = ContactForm(
            initial={'first_name': contact.first_name, 'last_name': contact.last_name, 'birthdate': contact.birthdate,
                     'sex': contact.sex, 'description': contact.description, 'avatar': contact.avatar})
        activites = Activity.objects.filter(activity_contact=contact)
        activity_form = ActivityForm()

        from_relationships = ContactRelationship.objects.filter(from_contact=contact)
        to_relationships = ContactRelationship.objects.filter(to_contact=contact)
        return render(request, 'contact.html',
                      {'form': form, 'id': id, 'activities': activites, 'activity_form': activity_form,
                       'from_relationships': from_relationships, 'to_relationships': to_relationships})

    def post(self, request, id):
        instance = Contact.objects.get(id=id)
        form = ContactForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            contact = Contact.objects.get(id=id)
            contact.updated_at = timezone.now()
            contact.save()
            return HttpResponseRedirect(f'/contact/view/{id}')
        return render(request, 'contact.html', {'form': form})


class ContactDelete(View):
    def get(self, request, id):
        contact = Contact.objects.get(id=id)
        contact.delete()
        return HttpResponseRedirect('/contacts/')


class ContactList(View):
    def get(self, request):
        user = request.user
        contacts_list1 = Contact.objects.filter(created_by=user).order_by('-updated_at')
        contacts1 = Contact.objects.filter(created_by=user).order_by('-updated_at')[0:1]
        contacts2 = Contact.objects.filter(created_by=user).order_by('-updated_at')[1:2]
        contacts3 = Contact.objects.filter(created_by=user).order_by('-updated_at')[2:]
        return render(request, 'contacts.html',
                      {'contacts_list1': contacts_list1, 'contacts1': contacts1, 'contacts2': contacts2,
                       'contacts3': contacts3})


class ContactListSort(View):
    def get(self, request, sort):
        user = request.user
        if sort == "newest_activity":
            contacts_list1 = Contact.objects.filter(created_by=user).order_by('-updated_at')
            contacts1 = Contact.objects.filter(created_by=user).order_by('-updated_at')[0:1]
            contacts2 = Contact.objects.filter(created_by=user).order_by('-updated_at')[1:2]
            contacts3 = Contact.objects.filter(created_by=user).order_by('-updated_at')[2:]
            return render(request, 'contacts.html',
                          {'contacts_list1': contacts_list1, 'contacts1': contacts1, 'contacts2': contacts2,
                           'contacts3': contacts3})
        if sort == "oldest_activity":
            contacts_list2 = Contact.objects.filter(created_by=user).order_by('updated_at')
            contacts1 = Contact.objects.filter(created_by=user).order_by('updated_at')[0:1]
            contacts2 = Contact.objects.filter(created_by=user).order_by('updated_at')[1:2]
            contacts3 = Contact.objects.filter(created_by=user).order_by('updated_at')[2:]
            return render(request, 'contacts.html',
                          {'contacts_list2': contacts_list2, 'contacts1': contacts1, 'contacts2': contacts2,
                           'contacts3': contacts3})
        contacts = Contact.objects.filter(created_by=user).order_by(sort)
        return render(request, 'contacts.html', {'contacts': contacts})


class ContactRelationshipCreate(View):
    def get(self, request, id):
        contact = Contact.objects.get(id=id)
        activities = Activity.objects.filter(activity_contact=contact)
        activity_form = ActivityForm()
        relationship_form = ContactRelationshipForm(my_arg=int(id), user=request.user)
        from_relationships = ContactRelationship.objects.filter(from_contact=contact)
        to_relationships = ContactRelationship.objects.filter(to_contact=contact)
        return render(request, 'contact.html',
                      {'contact': contact, 'relationship_form': relationship_form, 'id': id, 'activities': activities,
                       'activity_form': activity_form,
                       'from_relationships': from_relationships, 'to_relationships': to_relationships})

    def post(self, request, id):
        relationship_form = ContactRelationshipForm(request.POST, my_arg=int(id), user=request.user)
        contact = Contact.objects.get(id=id)
        activities = Activity.objects.filter(activity_contact=contact)
        activity_form = ActivityForm()
        from_relationships = ContactRelationship.objects.filter(from_contact=contact)
        to_relationships = ContactRelationship.objects.filter(to_contact=contact)

        if relationship_form.is_valid():
            types = relationship_form.cleaned_data['types']
            to_contact = relationship_form.cleaned_data['contact']
            if RelationshipType.objects.filter(to_type=types).exists():
                type_1 = RelationshipType.objects.get(to_type=types)
                new_relationship = ContactRelationship.objects.create(types=type_1, from_contact=contact,
                                                                      to_contact=to_contact)
                contact = Contact.objects.get(id=id)
                contact.updated_at = timezone.now()
                contact.save()

            else:
                type_2 = RelationshipType.objects.get(from_type=types)
                new_relationship = ContactRelationship.objects.create(types=type_2, from_contact=to_contact,
                                                                      to_contact=contact)
                contact = Contact.objects.get(id=id)
                contact.updated_at = timezone.now()
                contact.save()
            return HttpResponseRedirect(f'/contact/view/{id}')

        return render(request, 'contact.html',
                      {'contact': contact, 'relationship_form': relationship_form, 'id': id, 'activities': activities,
                       'activity_form': activity_form,
                       'from_relationships': from_relationships, 'to_relationships': to_relationships})


class RelationshipTypeCreate(View):
    def get(self, request):
        relationshiptype_form = RelationshipTypeForm()
        relationshiptypes = RelationshipType.objects.all()
        return render(request, 'relationships.html',
                      {'relationshiptype_form': relationshiptype_form, 'relationshiptypes': relationshiptypes})

    def post(self, request):
        relationshiptype_form = RelationshipTypeForm(request.POST)
        if relationshiptype_form.is_valid():
            name = relationshiptype_form.cleaned_data['name']
            from_type = relationshiptype_form.cleaned_data['from_type']
            to_type = relationshiptype_form.cleaned_data['to_type']
            relationshiptype = RelationshipType.objects.create(name=name, from_type=from_type, to_type=to_type)
            return HttpResponseRedirect('/relationships')
        return render(request, 'relationships.html', {'relationshiptype_form': relationshiptype_form})


class ContactRelationshipDelete(View):
    def get(self, request, type, id, id2, id3):
        contact = Contact.objects.get(id=id)
        contact2 = Contact.objects.get(id=id2)
        relationship = RelationshipType.objects.get(id=id3)
        if type == "from":
            ContactRelationship.objects.filter(types=relationship, from_contact=contact, to_contact=contact2).delete()
            contact = Contact.objects.get(id=id)
            contact.updated_at = timezone.now()
            contact.save()
            return HttpResponseRedirect(f"/contact/view/{id}")
        ContactRelationship.objects.filter(types=relationship, from_contact=contact2, to_contact=contact).delete()
        contact = Contact.objects.get(id=id)
        contact.updated_at = timezone.now()
        contact.save()
        return HttpResponseRedirect(f"/contact/view/{id}")


class SearchResult(View):
    def get(self, request):
        user = request.user
        name = request.GET.get('name', '')
        contacts = Contact.objects.filter(last_name__icontains=name, created_by=user)
        # contacts = Contact.objects.all()
        return render(request, 'contacts.html', {'contacts': contacts})


class UserLogin(View):
    def get(self, request):
        form = LoginForm
        next = request.GET.get('next')

        return render(request, 'login.html', {'form': form, 'next': next})

    def post(self, request):
        form = LoginForm(request.POST)

        # if
        # next = request.GET.get('next')
        # if next:
        #     return HttpResponse(next)
        # return HttpResponseRedirect(request.POST.get('next'))
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # return render(request, 'success.html', {'user': user})
                return HttpResponseRedirect("/")

        return render(request, 'login.html', {'form': form, 'error': "Błędne dane"})


class UserLogout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class CreateUser(View):
    def get(self, request):
        form = CreateUserForm
        return render(request, 'create_user.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            name = form.cleaned_data["name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            user = User.objects.create_user(username, email=email, first_name=name, last_name=last_name,
                                            password=password2)
            login(request, user)
            return HttpResponseRedirect("/")
        return render(request, 'create_user.html', {'form': form})


class ForgottenPassword(PermissionRequiredMixin, View):
    # permission_required = "auth.change_user"

    def get(self, request):
        form = ForgottenPasswordForm
        return render(request, 'forgotten_password.html', {'form': form})

    def post(self, request):
        form = ForgottenPasswordForm(request.POST)
        user = request.user
        if form.is_valid():
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            user.set_password(password2)
            user.save()
            logout(request)
            return HttpResponseRedirect("/login/")
        return render(request, 'forgotten_password.html', {'form': form})


class RenderPDF(View):
    def get(self, request, id):
        contact = Contact.objects.get(id=id)
        activites = Activity.objects.filter(activity_contact=contact).order_by('-created_at')
        from_relationships = ContactRelationship.objects.filter(from_contact=contact)
        to_relationships = ContactRelationship.objects.filter(to_contact=contact)
        params = {'contact': contact, 'activites': activites,
                  'from_relationships': from_relationships, 'to_relationships': to_relationships}
        # return Render.render('contact/pdf.html',

        return Render.render('pdf.html', params)
    # ids = request.GET.get('id')
    # cid = request.GET.get('cid')
    # sales = Invoice.objects.filter(pk=ids).select_related('projectid')
    # project = Project.objects.filter(pk=cid).select_related('clientname')
    # params = {
    #     'sales': sales,
    #     'request': request,
    #     'project': project
    # }
    # return Render.render('billing/pdf.html', params)
