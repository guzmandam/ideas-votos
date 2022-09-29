from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import secrets

from .utils import custom_id

class Poll(models.Model):
    id = models.CharField(
        primary_key=True, 
        max_length=11,
        unique=True,
        default=custom_id
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    
    def user_can_vote(self, user):
        """Return false if user has already voted

        Args:
            user (User)
        Returns:
            boolean: True if can vote, otherwise, False
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True
    
    @property
    def get_vote_count(self):
        """Generate vote count for actual poll

        Returns:
            int: Vote count
        """
        return self.vote_set.count()
    
    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['rgb(255, 205, 86)', 'rgb(54, 162, 235)', 'rgb(255, 99, 132)',
                           'rgb(59, 173, 2)', 'rgb(189, 0, 145)', 'rgb(234, 255, 0)', 'rgb(79, 64, 214)']

            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
            
        return res

    def __str__(self):
        return self.text
    
class Choice(models.Model):
    id = models.CharField(
        primary_key=True, 
        max_length=11,
        unique=True,
        default=custom_id
    )
    poll = models.ForeignKey(
        Poll, 
        on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'