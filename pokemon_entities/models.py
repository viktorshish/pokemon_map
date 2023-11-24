from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=200,
        verbose_name='Название на русском',
    )
    title_en = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Название на английском',
    )
    title_jp = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Название на японском',
    )
    image = models.ImageField(
        upload_to='pokemons',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self',
        related_name='next_evolutions',
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
        related_name='pokemon_entity',
        verbose_name='Покемон'
        )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время появления'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время исчезновения'
    )
    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon} {self.lat} {self.lon} {self.level}'
