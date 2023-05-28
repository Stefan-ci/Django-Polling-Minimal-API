from django.db import models
from django.urls import reverse
from django.utils.text import slugify



class Poll(models.Model):
    question = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Poll"
        verbose_name_plural = "Polls"
        ordering = ["-created_on", "question"]
    
    
    def __str__(self) -> str:
        return self.question


    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.question)
        super(Poll, self).save(*args, **kwargs)
    
    def get_absolute_url(self) -> str:
        return reverse("polls:polls-detail", kwargs={
            "slug": self.slug,
            "pk": self.pk
        })
    
    
    def answers(self) -> list:
        return self.answer_set.filter(is_active=True).order_by("answer")
    
    def similar_polls(self):
        return Poll.objects.filter(question__icontains=self.question).exclude(pk=self.pk).order_by("created_on")

    def count_all_answers(self) -> int:
        return self.answer_set.count()
    
    def count_active_answers(self) -> int:
        return self.answer_set.filter(is_active=True).count()







class Answer(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ["-created_on", "answer"]
    
    
    def __str__(self) -> str:
        return self.answer
