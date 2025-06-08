from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

#--------------------------------------------------

class Story(models.Model):
    title                = models.CharField(max_length=200)
    description          = models.TextField()
    author               = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public            = models.BooleanField(default=True)
    allow_contributions  = models.BooleanField(default=True)
    created_on           = models.DateTimeField(auto_now_add=True)

    # highest-rated chapter helper (for homepage / detail view)
    @property
    def top_chapter(self):
        """
        Returns the chapter with the highest average rating.
        Tie-break on newest.
        """
        return (
            self.chapters
                .annotate(avg=Avg("ratings__value"))
                .order_by("-avg", "-created_on")
                .first()
        )

    def __str__(self):
        return self.title

#--------------------------------------------------

class Chapter(models.Model):
    story       = models.ForeignKey(Story, on_delete=models.CASCADE,
                                    related_name="chapters")
    title       = models.CharField(max_length=200)
    content     = models.TextField()
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    parent      = models.ForeignKey(
        "self", on_delete=models.CASCADE,
        null=True, blank=True, related_name="children"
    )
    created_on  = models.DateTimeField(auto_now_add=True)

    # average rating calculation for templates
    @property
    def average_rating(self):
        """
        Returns float average (0-5). If no ratings, returns 0.
        """
        return self.ratings.aggregate(avg=Avg("value"))["avg"] or 0

    def __str__(self):
        return f"{self.title} (Story: {self.story.title})"


#--------------------------------------------------

class Rating(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars

    class Meta:
        unique_together = ('chapter', 'user')

    def __str__(self):
        return f"{self.chapter} rated {self.value} by {self.user.username}"

#--------------------------------------------------
    
@property
def average_rating(self):
    return self.ratings.aggregate(Avg('value'))['value__avg'] or 0