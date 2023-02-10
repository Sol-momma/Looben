from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404  
from django.http import JsonResponse

from .models import ReviewOfUniversity
from .forms import ReviewForm

from accounts.models import Schools, FollowForUser
from accounts import contribution_calculation
from chat.models import ConversationPartner
from notifications.models import Notification


@login_required
def create_review_of_university(request):
    create_review_form = ReviewForm(request.POST or None)
    if create_review_form.is_valid():
        create_review_form.instance.user = request.user
        create_review_form.save()
        messages.success(request, 'レビューを作成しました')
        # Start -Schoolsの星評価にこのレビューの評価を反映させる-
        target_university = Schools.objects.get(id=create_review_form.cleaned_data.get('university').id)
        review_list_for_target_university = ReviewOfUniversity.objects.filter(university=target_university).all()
        # get the value of total added rating
        total_added_rating_value = int(create_review_form.cleaned_data.get('star'))
        number_of_review = len(review_list_for_target_university) + 1
        for review in review_list_for_target_university:
            total_added_rating_value += int(review.star)
        target_university.star_rating = total_added_rating_value / number_of_review
        target_university.save()
        # End -Schoolsの星評価にこのレビューの評価を反映させる-
        contribution_calculation.for_creating_review(user=request.user)
        # フォロワーへ口コミ作成の通知を作成
        for follow in FollowForUser.objects.filter(followed_user=request.user).all():
            create_review_notification = Notification(sender=request.user, receiver=follow.user, message= str(request.user.username) + 'が新しく口コミを投稿しました。')
            create_review_notification.save()
        return redirect('accounts:research_university')
    notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
    number_of_notification =  Notification.objects.filter(receiver=request.user).count()
    has_notifications =  Notification.objects.filter(receiver=request.user).exists()
    has_not_seen_message = ConversationPartner.objects.filter(current_user=request.user, have_new_message=True).exists()
    return render(
        request, 'reviews/create_review_of_university.html', context={
            'create_review_form': create_review_form,
            'notification_lists': notification_lists,
            'number_of_notification': number_of_notification,
            'has_notifications': has_notifications,
            'has_not_seen_message': has_not_seen_message
        }
    )
    
    
class ReviewListOfUniversities(DetailView):
    model = Schools
    template_name = 'reviews/review_list_of_universities.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = self.object
        context['reviews'] = ReviewOfUniversity.objects.filter(university=school)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context


class CheckForUserMatchMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        target_review = get_object_or_404(ReviewOfUniversity, pk=self.kwargs['pk'])
        return self.request.user == target_review.user
        
    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Only user who made this author have access to this view'}
        )
    
    
class DeleteReviewView(CheckForUserMatchMixin, DeleteView):
    template_name = 'reviews/delete_review.html'
    model = ReviewOfUniversity
    
    def get_success_url(self):
        return reverse_lazy('dashboard:review_in_dashboard', kwargs={'username': self.object.user.username})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context