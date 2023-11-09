import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    moscow_time = timezone.localtime(
        timezone=timezone.pytz.timezone('Europe/Moscow')
        )
    pokemon_entitys = PokemonEntity.objects.filter(
        appeared_at__lte=moscow_time,
        disappeared_at__gt=moscow_time
    )
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon_entitys:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.image:
            image_url = pokemon.image.url
        else:
            image_url = None

        pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title_ru,
                'img_url': image_url,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)

    if pokemon.image:
        image_url = pokemon.image.url
    else:
        image_url = None

    pokemon_on_page = {
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': image_url,
        'description': pokemon.description
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    moscow_time = timezone.localtime(
        timezone=timezone.pytz.timezone('Europe/Moscow')
        )
    pokemon_entitys = pokemon.pokemon_entity.filter(
        appeared_at__lte=moscow_time,
        disappeared_at__gt=moscow_time
    )
    for pokemon_entity in pokemon_entitys:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })
