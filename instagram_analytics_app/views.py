import datetime
import os
import shutil
import zipfile

from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from get_followers_info import *
from get_personal_info import *
from instagram_analytics_app.forms import *


class InstagramAnalyticsIndexView(FormView):
    template_name = 'index.html'
    form_class = UploadZipForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        file = form.cleaned_data['fileToUpload']
        if zipfile.is_zipfile(file) is False:
            messages.error(self.request, 'Please upload a valid zip file!')
            return super().form_invalid(form)
        datetime_upload = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        folder_name = os.path.join('data', datetime_upload)
        file_path = os.path.join(folder_name, file.name)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(folder_name)
        os.remove(file_path)
        messages.success(self.request, f'Data archive {file.name} uploaded successfully at {datetime.datetime.now().strftime("%H:%M:%S, %d.%m.%Y")}.')
        return super().form_valid(form)


class FollowersAnalyticsView(View):
    template = loader.get_template('followers_analytics.html')
    success_url = reverse_lazy('followers_analytics')

    def get_followers_context(self):
        data_dirs = os.listdir('data')
        context = {
            'followers_list': '',
            'followers_list_count': 0,
            'followings_list': '',
            'followings_list_count': 0,
            'mutual_followers': '',
            'mutual_followers_count': 0,
            'not_following_me_back': '',
            'not_following_me_back_count': 0,
            'i_dont_follow_back': '',
            'i_dont_follow_back_count': 0,
            'account': '',
            'full_name': '',
            'profile_picture_uri': '',
            'search_followers': '',
            'search_followings': '',
            'search_mutual_followers': '',
            'search_not_following_me_back': '',
            'search_i_dont_follow_back': '',
        }
        if len(data_dirs) > 0:
            data_dirs.sort(reverse=True)
            data_dir = os.path.join('data', data_dirs[0])
            followers_list = get_followers_list(data_dir)
            followings_list = get_followings_list(data_dir)
            mutual_followers = get_mutual_followers(followers_list, followings_list)
            not_following_me_back = get_not_following_me_back(followers_list, followings_list)
            i_dont_follow_back = get_i_dont_follow_back(followers_list, followings_list)
            account, full_name, profile_picture_uri = get_personal_info(data_dir)
            if not os.path.exists('instagram_analytics_app/static/profile_pictures'):
                os.makedirs('instagram_analytics_app/static/profile_pictures')
            shutil.copyfile(profile_picture_uri, os.path.join('instagram_analytics_app', 'static', 'profile_pictures', account.replace(".", "") + '.jpg'))
            profile_picture_uri = os.path.join('/static', "profile_pictures", account.replace(".", "") + '.jpg').replace("\\", "/")
            context['followers_list'] = followers_list
            context['followers_list_count'] = len(followers_list)
            context['followings_list'] = followings_list
            context['followings_list_count'] = len(followings_list)
            context['mutual_followers'] = mutual_followers
            context['mutual_followers_count'] = len(mutual_followers)
            context['not_following_me_back'] = not_following_me_back
            context['not_following_me_back_count'] = len(not_following_me_back)
            context['i_dont_follow_back'] = i_dont_follow_back
            context['i_dont_follow_back_count'] = len(i_dont_follow_back)
            context['account'] = account
            context['full_name'] = full_name
            context['profile_picture_uri'] = profile_picture_uri
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_followers_context()
        return HttpResponse(self.template.render(context, request))

    def post(self, request, *args, **kwargs):
        context = self.get_followers_context()
        old_context = context.copy()
        followers_list_form = FollowersListForm(request.POST)
        followings_list_form = FollowingsListForm(request.POST)
        mutual_followers_list_form = MutualFollowersListForm(request.POST)
        not_following_me_back_list_form = NotFollowingMeBackListForm(request.POST)
        i_dont_follow_back_list_form = IDontFollowBackListForm(request.POST)
        if followers_list_form.is_valid():
            search_term = followers_list_form.cleaned_data['search_follower']
            context['search_followers'] = search_term
            context['search_followings'] = ''
            context['search_mutual_followers'] = ''
            context['search_not_following_me_back'] = ''
            context['search_i_dont_follow_back'] = ''
            context['followers_list'] = search_accounts(search_term, old_context['followers_list'])
            context['followings_list'] = old_context['followings_list']
            context['mutual_followers'] = old_context['mutual_followers']
            context['not_following_me_back'] = old_context['not_following_me_back']
            context['i_dont_follow_back'] = old_context['i_dont_follow_back']
        if followings_list_form.is_valid():
            search_term = followings_list_form.cleaned_data['search_following']
            context['search_followers'] = ''
            context['search_followings'] = search_term
            context['search_mutual_followers'] = ''
            context['search_not_following_me_back'] = ''
            context['search_i_dont_follow_back'] = ''
            context['followers_list'] = old_context['followers_list']
            context['followings_list'] = search_accounts(search_term, old_context['followings_list'])
            context['mutual_followers'] = old_context['mutual_followers']
            context['not_following_me_back'] = old_context['not_following_me_back']
            context['i_dont_follow_back'] = old_context['i_dont_follow_back']
        if mutual_followers_list_form.is_valid():
            search_term = mutual_followers_list_form.cleaned_data['search_mutual_follower']
            context['search_followers'] = ''
            context['search_followings'] = ''
            context['search_mutual_followers'] = search_term
            context['search_not_following_me_back'] = ''
            context['search_i_dont_follow_back'] = ''
            context['followers_list'] = old_context['followers_list']
            context['followings_list'] = old_context['followings_list']
            context['mutual_followers'] = search_accounts(search_term, old_context['mutual_followers'])
            context['not_following_me_back'] = old_context['not_following_me_back']
            context['i_dont_follow_back'] = old_context['i_dont_follow_back']
        if not_following_me_back_list_form.is_valid():
            search_term = not_following_me_back_list_form.cleaned_data['search_not_following_me_back']
            context['search_followers'] = ''
            context['search_followings'] = ''
            context['search_mutual_followers'] = ''
            context['search_not_following_me_back'] = search_term
            context['search_i_dont_follow_back'] = ''
            context['followers_list'] = old_context['followers_list']
            context['followings_list'] = old_context['followings_list']
            context['mutual_followers'] = old_context['mutual_followers']
            context['not_following_me_back'] = search_accounts(search_term, old_context['not_following_me_back'])
            context['i_dont_follow_back'] = old_context['i_dont_follow_back']
        if i_dont_follow_back_list_form.is_valid():
            search_term = i_dont_follow_back_list_form.cleaned_data['search_i_dont_follow_back']
            context['search_followers'] = ''
            context['search_followings'] = ''
            context['search_mutual_followers'] = ''
            context['search_not_following_me_back'] = ''
            context['search_i_dont_follow_back'] = search_term
            context['followers_list'] = old_context['followers_list']
            context['followings_list'] = old_context['followings_list']
            context['mutual_followers'] = old_context['mutual_followers']
            context['not_following_me_back'] = old_context['not_following_me_back']
            context['i_dont_follow_back'] = search_accounts(search_term, old_context['i_dont_follow_back'])
        return HttpResponse(self.template.render(context, request))
