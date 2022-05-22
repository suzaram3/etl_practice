"""
Author : Mitch Suzara <suzaram3@gmail.com>
Date   : 2022-05-12
Purpose: Generate word cloud from top artists in data pipeline
"""
import csv, logging, logging.config, random, sys
from configparser import ConfigParser, ExtendedInterpolation

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from wordcloud import WordCloud

logging.config.fileConfig("../logging.conf")
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(["../db.conf", "../settings.conf"])

file_logger = logging.getLogger("file")


def grey_color_func(
    word, font_size, position, orientation, random_state=None, **kwargs
):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


def csv_frequency(file_path: str) -> dict:
    frequency_dict = {}
    with open(file_path, newline="") as csvfile:
        music_reader = csv.reader(csvfile, delimiter="|")
        next(music_reader, None)
        for k, v in music_reader:
            frequency_dict[k] = int(v)
    return frequency_dict


def generate_word_cloud(frequency_dict: dict, file_path: str, mask_image: str):
    mask = np.array(Image.open(mask_image))
    wc = WordCloud(
        font_path=config["mask_fonts"]["wordcloud_font"], mask=mask, max_font_size=256
    ).generate_from_frequencies(frequency_dict)

    plt.imshow(
        wc.recolor(color_func=grey_color_func, random_state=3),
        interpolation="bilinear",
    )

    plt.axis("off")
    plt.savefig(
        file_path,
        bbox_inches="tight",
        pad_inches=0,
        dpi=1200,
    )


def usage() -> str:
    print(f"Usage: {sys.argv[0]} [artists|songs]")


def main():
    options = [option for option in config["mask_images"]]
    random_mask = random.choice(options)
    if len(sys.argv) < 2:
        usage()
    elif sys.argv[1] == "artists":
        generate_word_cloud(
            csv_frequency(config["file_paths"]["top_artists_csv"]),
            config["file_paths"]["top_artists_png"],
            config["mask_images"][random_mask],
        )
        file_logger.info(f"Top artist word cloud made with {random_mask}")

    elif sys.argv[1] == "songs":
        generate_word_cloud(
            csv_frequency(config["file_paths"]["top_songs_csv"]),
            config["file_paths"]["top_songs_png"],
            config["mask_images"][random_mask],
        )
        file_logger.info(f"Top artist word cloud made with {random_mask}")
    else:
        usage()


if __name__ == "__main__":
    main()
