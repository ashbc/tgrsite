from django.db import models
from django.core import validators
from django.shortcuts import reverse

from users.models import Member
from messaging.models import MessageThread


# Create your models here.
class Rpg(models.Model):
    game_masters = models.ManyToManyField(Member, related_name='rpgs_running', blank=True,
                                          help_text="Who is actually running the event")
    title = models.CharField(max_length=64, verbose_name='Name', help_text="The event's name")
    system = models.CharField(max_length=64, blank=True, help_text="The system that is being used")
    description = models.TextField(max_length=8192, blank=True, help_text="Longform description")
    timeslot = models.CharField(max_length=64, blank=True, help_text="The date/time(s) this event will occur")
    location = models.CharField(max_length=64, blank=True, help_text="The location where this event will occur")
    players_wanted = models.PositiveSmallIntegerField(validators=[validators.MinValueValidator(1)])
    is_in_the_past = models.BooleanField(default=False, help_text="Has the event already happened?")
    finishes = models.DateField(blank=True, null=True,
                                help_text="A date after which it should be automatically marked as finished")

    created_at = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False, help_text='Pin this event to the top of the list')
    unlisted = models.BooleanField(default=False, help_text='Prevent this from appearing on the events listing')
    creator = models.ForeignKey(Member, related_name='rpgs_owned', on_delete=models.PROTECT,
                                help_text="The creator of this event")
    members = models.ManyToManyField(Member, blank=True, help_text="The people playing the game")
    tags = models.ManyToManyField('Tag')
    discord = models.BooleanField(default=False,
                                  help_text="Require users to have a discord username listed before signing up")
    member_only = models.BooleanField(default=False,
                                      help_text="Require users to be verified members to sign up")
    messaging_thread = models.ForeignKey(MessageThread, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def tags_str(self):
        return ', '.join([str(x) for x in self.tags.all()])

    def get_absolute_url(self):
        return reverse("rpgs:detail", args=[self.pk])


class Tag(models.Model):
    name = models.CharField(max_length=72)

    def __str__(self):
        return self.name
