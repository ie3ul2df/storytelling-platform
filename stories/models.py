from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save

#--------------------------------------------------

class Story(models.Model):
    title                = models.CharField(max_length=200)
    description          = models.TextField()
    author               = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public            = models.BooleanField(default=True)
    allow_contributions  = models.BooleanField(default=True)
    created_on           = models.DateTimeField(auto_now_add=True)
    # image                = models.ImageField(upload_to='stories/', blank=True, null=True)
    image = CloudinaryField(
        'image',
        default='default-story-image_ttrfqb',
        blank=True,
        null=True
    )

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
    
    @property
    def first_slide_chapters(self):
        """
        For each root chapter (parent=None), get the highest-rated child.
        If no children, fallback to root.
        """
        roots = self.chapters.filter(parent=None).order_by('created_on')
        best_chapters = []

        for root in roots:
            children = list(root.children.all().annotate(avg_rating=Avg('ratings__value')))

            # include root in comparison too
            root.avg_rating = root.average_rating
            all_versions = [root] + children

            best = max(all_versions, key=lambda ch: ch.avg_rating or 0)
            best_chapters.append(best)

        return best_chapters

    @property
    def total_rank(self):
        """
        Calculates the average of the ratings of the best chapters across all branches.
        """
        chapters = self.first_slide_chapters
        if not chapters:
            return 0
        # return sum(ch.average_rating for ch in chapters) / len(chapters)
        return round(sum(ch.average_rating for ch in chapters) / len(chapters), 2)
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

#--------------------------------------------------

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_image = models.ImageField(upload_to='profiles/', default='default-profile.png')
    profile_image = CloudinaryField(
        'image',
        default='default-profile-image_oe2lqb',
        blank=True,
        null=True
    )

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()