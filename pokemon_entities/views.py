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
    if image_url is not None:
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
    pokemons = Pokemon.objects.all()

    moscow_time = timezone.localtime(
        timezone=timezone.pytz.timezone('Europe/Moscow')
        )
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=moscow_time,
        disappeared_at__gt=moscow_time
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_on_page = []
    for pokemon in pokemons:
        image_url = pokemon.image.url if pokemon.image else None
        pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title_ru,
                'img_url': image_url,
            })

    for pokemon_entity in pokemon_entities:
        entity_image_url = pokemon_entity.pokemon.image.url if pokemon_entity.pokemon.image else None
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(entity_image_url),
        )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    image_url = requested_pokemon.image.url if requested_pokemon.image else None
    pokemon_on_page = {
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'img_url': image_url,
        'description': requested_pokemon.description,
    }

    if requested_pokemon.previous_evolution:
        previous_evolution_pokemon = {
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': requested_pokemon.previous_evolution.image.url if requested_pokemon.previous_evolution.image else None,
            'title_ru': requested_pokemon.previous_evolution.title_ru,
        }
        pokemon_on_page['previous_evolution'] = previous_evolution_pokemon

    next_evolution_pokemon = requested_pokemon.next_evolutions.first()
    if next_evolution_pokemon:
        next_evolution_pokemons = {
            'pokemon_id': next_evolution_pokemon.id,
            'img_url': next_evolution_pokemon.image.url if next_evolution_pokemon.image else None, 
            'title_ru': next_evolution_pokemon.title_ru,
        }
        pokemon_on_page['next_evolution'] = next_evolution_pokemons

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    moscow_time = timezone.localtime(
        timezone=timezone.pytz.timezone('Europe/Moscow')
        )
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=requested_pokemon,
        appeared_at__lte=moscow_time,
        disappeared_at__gt=moscow_time
    )
    for pokemon_entity in pokemon_entities:
        image_url = pokemon_entity.pokemon.image.url if pokemon_entity.pokemon.image else None
        add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(image_url),
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })
