"""
XOR lookups

To perform an XOR lookup, or a lookup that combines ANDs and XORs, combine
``QuerySet`` objects using ``&`` and ``^`` operators.

Alternatively, use positional arguments, and pass one or more expressions of
clauses using the variable ``django.db.models.Q``.
"""

from django.db import models


class Number(models.Model):
    num = models.IntegerField()
    other_num = models.IntegerField(null=True)
    another_num = models.IntegerField(null=True)

    def __str__(self):
        return str(self.num)

    class Meta:
        ordering = ('num', )
