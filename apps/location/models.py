from django.db import models
from apps.core.models import BaseModel


class State(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class City(BaseModel):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("name", "state")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, {self.state.name}"
