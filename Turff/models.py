from django.db import models


from django.contrib.auth.models  import User

from django.db.models.functions import Coalesce
from django.db.models import Sum, F
import datetime

# Create your models here.


class TimeSlot(models.Model):
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    day = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    status = (
        ('available', 'available'),
        ('not available', 'not available'))
    status = models.CharField(choices=status, default="available", max_length=20)

    class Meta:
        unique_together = ('day', 'start_time','end_time','status',)

    def __str__(self):
        return f" {self.day} - {str(self.start_time)} - {str(self.end_time)} "
    

class Ground(models.Model):
    image = models.ImageField(upload_to="images", null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    class Meta:
        unique_together = ('name', 'address',)

    def __str__(self):
        return self.name

class Pitch(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images", null=True)
    ground = models.ForeignKey(Ground, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return self.name

class BookingDates(models.Model):

    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    timeslot = models.ManyToManyField(TimeSlot)

    class Meta:
        unique_together = ('startdate', 'enddate','pitch')

    def __str__(self):
        return f" {str(self.startdate)} - {str(self.enddate)}" 
        
    def timeslot_price(self):
        instance = self.timeslot.all()
        print(instance)
        sum = 0
        for i in instance:
            # print(i.price)
            sum += i.price
            
        return sum

        

    # def total_price():
    #     instance = BookingDates.objects.all()
    #     print(instance)
    #     sum = 0
    #     for i in instance:
    #         sum += i.timeslot.price
    #         print(sum)

    #     return sum

      

class Booking(models.Model):

    bookingdate_id = models.ManyToManyField(BookingDates)
    cust_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = (
        ('available', 'available'),
        ('taken', 'taken'))
    status = models.CharField(choices=status, default="available", max_length=20)
    amount = models.PositiveIntegerField(default=0)
   

    def total_price(self):
        instance = self.bookingdate_id.all()
        print(instance)
    
        sum = 0
        for i in instance:
            # print(i.timeslot)
         
            sum += i.timeslot_price()
            # print(sum)

        return sum



class Teams(models.Model):
    team_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images", null=True)
    total_matches = models.PositiveIntegerField(null=True,blank=True)
    points = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.team_name

    

    @property
    def group_home_matches(self):
        return self.home_matches

    @property
    def group_away_matches(self):
        return self.away_matches


    # @property
    def games_played(self):
        return self.group_home_matches.count() + self.group_away_matches.count()

    @property
    def goals_for(self):
        home_goals = self.group_home_matches.aggregate(sum=Coalesce(Sum('home_goals'), 0))
        away_goals = self.group_away_matches.aggregate(sum=Coalesce(Sum('away_goals'), 0))
        return home_goals['sum'] + away_goals['sum']

    @property
    def goals_against(self):
        home_goals_conceeded = self.group_home_matches.aggregate(sum=Coalesce(Sum('away_goals'), 0))
        away_goals_conceeded = self.group_away_matches.aggregate(sum=Coalesce(Sum('home_goals'), 0))
        return home_goals_conceeded['sum'] + away_goals_conceeded['sum']

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    @property
    def wins(self):
        home_wins = self.group_home_matches.filter(home_goals__gt=F('away_goals'), started=True).count()
        away_wins = self.group_away_matches.filter(away_goals__gt=F('home_goals'), started=True).count()
        return home_wins + away_wins

    @property
    def losses(self):
        home_losses = self.group_home_matches.filter(home_goals__lt=F('away_goals'), started=True).count()
        away_losses = self.group_away_matches.filter(away_goals__lt=F('home_goals'), started=True).count()
        return home_losses + away_losses

    @property
    def draws(self):
        home_draws = self.group_home_matches.filter(home_goals=F('away_goals'), started=True).count()
        away_draws = self.group_away_matches.filter(away_goals=F('home_goals'), started=True).count()
        return home_draws + away_draws

    @property
    def points(self):
        """
        Return the total points total
        :return:
        """
        return self.wins * 3 + self.draws * 1

class League(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images",null=True)
    
    def __str__(self):
        return self.name

class Match(models.Model):
    match_name = models.CharField(max_length=100)
    league = models.ForeignKey(League,on_delete=models.CASCADE)
    dates = models.ForeignKey(BookingDates, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Teams, on_delete=models.SET_NULL, related_name='home_matches', null=True, blank=True)
    away_team = models.ForeignKey(Teams, on_delete=models.SET_NULL, related_name='away_matches', null=True, blank=True)

    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)
 
    status = (
        ("Scheduled","Scheduled"),
        ("Started","Started"),
        ("Completed","Completed")
     
    )           
    status = models.CharField(choices=status, default="Scheduled",max_length=50)       
    duration = models.CharField(max_length=20)

    def __str__(self):
        return self.match_name


    class Meta:
        unique_together = ('match_name', 'dates')        
        
    # @property
    # def find_match_name(self):
    #     instance = self.teams.all()
    #     for i in instance:
    #         return i
        
        # return i


    # @property
    # def games_played(self):
    #     return self.group_home_matches.count() + self.group_away_matches.count()

    # @property
    # def goals_for(self):
    #     home_goals = self.group_home_matches.aggregate(sum=Coalesce(Sum('home_goals'), 0))
    #     away_goals = self.group_away_matches.aggregate(sum=Coalesce(Sum('away_goals'), 0))
    #     return home_goals['sum'] + away_goals['sum']

    # @property
    # def goals_against(self):
    #     home_goals_conceeded = self.group_home_matches.aggregate(sum=Coalesce(Sum('away_goals'), 0))
    #     away_goals_conceeded = self.group_away_matches.aggregate(sum=Coalesce(Sum('home_goals'), 0))
    #     return home_goals_conceeded['sum'] + away_goals_conceeded['sum']

    # @property
    # def goal_difference(self):
    #     return self.goals_for - self.goals_against

    # @property
    # def wins(self):
    #     home_wins = self.group_home_matches.filter(home_goals__gt=F('away_goals'), started=True).count()
    #     away_wins = self.group_away_matches.filter(away_goals__gt=F('home_goals'), started=True).count()
    #     return home_wins + away_wins

    # @property
    # def losses(self):
    #     home_losses = self.group_home_matches.filter(home_goals__lt=F('away_goals'), started=True).count()
    #     away_losses = self.group_away_matches.filter(away_goals__lt=F('home_goals'), started=True).count()
    #     return home_losses + away_losses

    # @property
    # def draws(self):
    #     home_draws = self.group_home_matches.filter(home_goals=F('away_goals'), started=True).count()
    #     away_draws = self.group_away_matches.filter(away_goals=F('home_goals'), started=True).count()
    #     return home_draws + away_draws

    # @property
    # def points(self):
    #     """
    #     Return the total points total
    #     :return:
    #     """
    #     return self.wins * 3 + self.draws * 1
    
        



