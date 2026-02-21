from __future__ import annotations

from django.db import models


class Menu(models.Model):
    name = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=300, blank=True, default="")
    named_url = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.title

