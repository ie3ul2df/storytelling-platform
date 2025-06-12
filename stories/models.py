from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save

# --------------------------------------------------
# ------------------ Story model with title, author, image, and rating helpers


class Story(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    allow_contributions = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField(
        "image", default="default-story-image_ttrfqb", blank=True, null=True
    )

    # highest-rated chapter helper (for homepage / detail view)
    @property
    def top_chapter(self):
        """
        Returns the chapter with the highest average rating.
        Tie-break on newest.
        """
        return (
            self.chapters.annotate(avg=Avg("ratings__value"))
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
        roots = self.chapters.filter(parent=None).order_by("created_on")
        best_chapters = []

        for root in roots:
            children = list(
                root.children.all().annotate(avg_rating=Avg("ratings__value"))
            )

            # include root in comparison too
            root.avg_rating = root.average_rating
            all_versions = [root] + children

            best = max(all_versions, key=lambda ch: ch.avg_rating or 0)
            best_chapters.append(best)

        return best_chapters

    @property
    def total_rank(self):
        """
        Combines average rating of top-rated chapters + direct story rating.
        """
        chapter_ratings = [
            ch.average_rating for ch in self.first_slide_chapters if ch.average_rating
        ]
        story_rating = self.average_rating  # direct story ratings (StoryRating)
        all_ratings = chapter_ratings + ([story_rating] if story_rating else [])
        if not all_ratings:
            return 0
        return round(sum(all_ratings) / len(all_ratings), 2)

    @property
    def average_rating(self):
        return self.ratings.aggregate(Avg("value"))["value__avg"] or 0


# --------------------------------------------------
# ------------------ Chapter model with parent-child structure and average rating


class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    created_on = models.DateTimeField(auto_now_add=True)

    # average rating calculation for templates
    @property
    def average_rating(self):
        """
        Returns float average (0-5). If no ratings, returns 0.
        """
        return self.ratings.aggregate(avg=Avg("value"))["avg"] or 0

    def __str__(self):
        return f"{self.title} (Story: {self.story.title})"


# --------------------------------------------------
# ------------------ Chapter rating model (1–5 stars), one per user


class Rating(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars

    class Meta:
        unique_together = ("chapter", "user")

    def __str__(self):
        return f"{self.chapter} rated {self.value} by {self.user.username}"


# --------------------------------------------------
# ------------------ Returns average rating or 0 if none


@property
def average_rating(self):
    return self.ratings.aggregate(Avg("value"))["value__avg"] or 0


# --------------------------------------------------
# ------------------ User profile with image, bio, follow system, and auto-creation


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField("image", blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True, verbose_name="About Me")
    contact_email = models.EmailField(blank=True)
    # Users this profile is following
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )

    def __str__(self):
        return self.user.username

    def is_following(self, other_profile):
        return self.following.filter(pk=other_profile.pk).exists()

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def profile_image_url(self):
        if not self.profile_image:
            return "https://res.cloudinary.com/ddo1eszpe/image/upload/v1749497011/default-profile-image_oe2lqb.jpg"
        return self.profile_image.url


# --------------------------------------------------
# ------------------ Auto-create or update UserProfile on User save


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


# --------------------------------------------------
# ------------------ Model for user rating a story (1 per user)


class StoryRating(models.Model):
    story = models.ForeignKey("Story", related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("story", "user")


# --------------------------------------------------
# ------------------ Model for user bookmarking a story (unique per user/story)


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="bookmarked_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "story")  # prevents duplicate bookmarks

    def __str__(self):
        return f"{self.user.username} bookmarked {self.story.title}"


# --------------------------------------------------
# ------------------ Model for story/chapter comments with reply and read tracking


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, null=True, blank=True, related_name="comments"
    )
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments",
    )
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # For author notification tracking

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user.username}"
