from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Blogs(models.Model):
    title=models.CharField(max_length=56)
    content=models.CharField(max_length=150)
    author=models.CharField(max_length=120)
    liked_by=models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Mobiles(models.Model):
    name=models.CharField(max_length=120,unique=True)
    price=models.PositiveIntegerField(default=5000)
    band=models.CharField(max_length=150,default="4g")
    display=models.CharField(max_length=120)
    processor=models.CharField(max_length=120)


    def __str__(self):
        return self.name

    def average_rating(self):
        reviews=self.reviews_set.all()
        if reviews:
            ratings=[rv.rating for rv in reviews]
            total=sum(ratings)
            return total/len(reviews)
        else:
            return 0
    def total_reviews(self):
        return self.reviews_set.all().count()



#primarykey ===> 1:1relationship
#Foreginkey ===> 1:M===>parent object delete ====>CASCADE

class Reviews(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Mobiles,on_delete=models.CASCADE)
    reviews=models.CharField(max_length=120)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    date=models.DateField(auto_now_add=True)

    class Meta:
        unique_together=("author","product")

    def __str__(self):
        return self.review

#Reviews.objects.create(author=user,product=produ,review=bad,rating=4)
#User.reviews_set(author=user,product=prod,reviews=good,rating=5)


class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Mobiles,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    options=(
        ("incart","incart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=120,choices=options,default="incart")

class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Mobiles,on_delete=models.CASCADE)
    options=(
        ("incart","incart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=120,choices=options,default="order-placed")
































#orm query for creating a resource(object relatonal mapping)
#modelname.objects.create(field1=value1,field2=value2,,,,,,,,,,)
#Blogs.objects.create(title="goodmorning",content="hello",author="ram",liked_by="hari")

#orm query for fecting all objects
#qs=modelsname.objects.all()
#qs=Blogs.objects.all()
#qs

#detail view of an specific object
#qs=modelname.objects.get(id=1)
