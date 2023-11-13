from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, null=True, blank=True)
    title_jp = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='pokemons', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        related_name='next_evolution',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Из кого эволюционирует',
        )

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_entity'
        )
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField()
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon} {self.lat} {self.lon} {self.level}'
