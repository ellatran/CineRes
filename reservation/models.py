from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.


class Film(models.Model):
    filmName = models.CharField(max_length=200)
    filmYear = models.CharField(max_length=4)
    filmDirector = models.CharField(max_length=50)
    filmCountry = models.CharField(max_length=50)
    filmActors = models.CharField(max_length=200)
    filmPlot = models.CharField(max_length=500)
    Trailer = models.CharField(max_length=100)
    poster = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.filmName


class Audi(models.Model):
    audiNumber = models.CharField(max_length=1)
    audiNoSeats = models.IntegerField(verbose_name=None)
    audiRows = models.IntegerField(verbose_name=None)

    def __str__(self):
        return self.audiNumber


class Screening(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    audi = models.ForeignKey(Audi, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    class Meta:
        unique_together = ["audi", "date_time"]

    def __str__(self):
        return str(self.film) + " -  Audi" + str(self.audi) + " - " + str(self.date_time)


class Booking(models.Model):
    Screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    purchaseDate = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + str(self.customer)


class Seat(models.Model):
    STA = (
        ('AVL', 'Available'),
        ('BLK', 'Blocked'),
        ('RSV', 'Reserved')
    )
    seatPos = models.CharField(max_length=3)
    Status = models.CharField(max_length=15, choices=STA, default='AVL')
    Screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "ScrID " + str(self.Screening_id) + " " + str(self.seatPos)


def create_seatmap(sender, **kwargs):
    letters = "ABCDEFGHIJ"
    if kwargs['created']:
        for letter in letters:
            for i in range(1,25):
               seat = Seat.objects.create(seatPos=str(i)+letter, Screening=kwargs['instance'])


post_save.connect(create_seatmap, sender=Screening)
