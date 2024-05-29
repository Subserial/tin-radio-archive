import datetime
import os

from string import Template

template = Template("""+++
title = "${name}"
date = ${isodate}
tags = ["Season ${season}", "The Basement", "WVUD", "Joseph's Show", "Tin Radio", "2021"]
+++

{{% audio src="/sets/${filename}" %}}

Scheduled as Joseph's Show on September 7th, 2021
Scheduled as Tin Radio on September 7th, 2021

Aired from 91.3 WVUD HD-2: The Basement U of D Student Radio
Aired from 91.3 WVUD: The Voice of the University of Delaware

Playlist/Spinitron: https://spinitron.com/WVUD-HD2/pl/14064543/Joseph-s-show
""")

with open("names.txt", "r") as file:
    titles = file.readlines()

for title in titles:
    target = (title.lower()
              .replace(" ", "_")
              .replace("(", "")
              .replace(")", "")
              .replace("'", "_")) + ".mp3"
    parts = title.split(" ")
    name = ' '.join(parts[5:]).strip()
    season = int(parts[2][1:])
    episode = int(parts[3][1:])
    isodate = (datetime.datetime.now() + datetime.timedelta(0, 3600 * (season + 9) + 120 * episode)).isoformat()
    content = template.substitute(
        name=name,
        season=season,
        filename=target,
        isodate=isodate,
    )
    season_dir = f"content/posts/s{season}"
    filename = f"content/posts/s{season}/e{episode}.md"
    if not os.path.isdir(season_dir):
        os.mkdir(season_dir)
    with open(filename, "w") as md:
        md.write(content)
