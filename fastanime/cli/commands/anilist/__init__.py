import click

from .favourites import favourites
from .recent import recent
from .search import search
from .popular import popular
from .trending import trending
from .upcoming import upcoming


commands = {
    "favourites": favourites,
    "recent": recent,
    "search": search,
    "popular": popular,
    "trending": trending,
    "upcoming": upcoming,
}


@click.group(commands=commands)
def anilist():
    pass