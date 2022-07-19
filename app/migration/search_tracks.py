import json
import os
from multiprocessing import Process, Queue
from SpotifyHistory.app.utils.spotify import SpotifyHandler
from SpotifyHistory.app.utils.queries import song_ids
from SpotifyHistory.config import Config
from SpotifyHistory.models.models import Album, Artist, Song, SongStreamed


def chunk_list(lst: list) -> list[list]:
    return [lst[i : i + MAX_RECORDS] for i in range(0, len(lst), MAX_RECORDS)]


def get_tracks(**kwargs) -> list[dict]:
    response = [sp.get_tracks_bulk(chunk) for chunk in kwargs["ids"]]
    # response = sp.get_tracks_bulk(kwargs['ids'][0])
    q.put(response)


MAX_RECORDS = 50
c, sp, q = Config(), SpotifyHandler(), Queue()
cpu_count = os.cpu_count()

song_ids = song_ids()

sub_list_len = len(song_ids) // cpu_count

cpu_chunk_list = [
    song_ids[i : i + sub_list_len] for i in range(0, len(song_ids), sub_list_len)
]

process_list = [chunk_list(chunk) for chunk in cpu_chunk_list]

pool = [
    Process(
        target=get_tracks,
        kwargs={
            "ids": process_list[0],
            "process": "p1",
        },
    ),
    Process(
        target=get_tracks,
        kwargs={
            "ids": process_list[1],
            "process": "p2",
        },
    ),
    Process(
        target=get_tracks,
        kwargs={
            "ids": process_list[2],
            "process": "p3",
        },
    ),
    Process(
        target=get_tracks,
        kwargs={
            "ids": process_list[3],
            "process": "p4",
        },
    ),
]

[p.start() for p in pool]
p_results = [q.get() for _ in range(cpu_count)]
[p.join() for p in pool]


with open("/home/msuzara/music_data/response.json", "w") as fo:
    json.dump(p_results, fo)
