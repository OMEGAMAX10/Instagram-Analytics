from django import forms


class UploadZipForm(forms.Form):
    fileToUpload = forms.FileField()


class FollowersListForm(forms.Form):
    search_follower = forms.CharField(max_length=40)


class FollowingsListForm(forms.Form):
    search_following = forms.CharField(max_length=40)


class MutualFollowersListForm(forms.Form):
    search_mutual_follower = forms.CharField(max_length=40)


class NotFollowingMeBackListForm(forms.Form):
    search_not_following_me_back = forms.CharField(max_length=40)


class IDontFollowBackListForm(forms.Form):
    search_i_dont_follow_back = forms.CharField(max_length=40)
