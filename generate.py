import datetime
import os

from string import Template

template = Template("""+++
title = "${name}"
date = ${isodate}
tags = [${tags}]
seasons = ["Season ${season}"]
seasons_weight = ${episode}
+++

{{% audio src="/sets/${filename}" %}}

${show} on ${longdate}

Aired on ${stationdesc}

Playlist/Spinitron: ${spinlink}
""")

with open("names.txt", "r") as file:
    titles = file.readlines()
with open("data.txt", "r") as file:
    data = file.readlines()

for i in range(len(titles)):
    title = titles[i].strip()
    datum = data[i]
    info = datum.split(';')
    station, show, date, link = info
    rawdate = datetime.datetime.fromisoformat(date)
    day = rawdate.day.real
    end = "th"
    if day % 10 == 1:
        end = "st"
    elif day % 10 == 2:
        end = "nd"
    airdate = rawdate.strftime(f"%A, %B {day}{end}, %Y")
    airyear = rawdate.strftime("%Y")
    airloc = "91.3 WVUD: The Voice of the University of Delaware"
    if station == "The Basement":
        airloc = "91.3 WVUD HD-2: The Basement U of D Student Radio"

    target = (title.lower()
              .replace(" ", "_")
              .replace("(", "")
              .replace(")", "")
              .replace("'", "_")) + ".mp3"
    parts = title.split(" ")
    name = ' '.join(parts[5:]).strip()
    season = int(parts[2][1:])
    episode = int(parts[3][1:])
    gendate = datetime.datetime.fromisoformat("2024-05-28")
    isodate = (gendate + datetime.timedelta(0, 3600 * (season + 9) + 120 * episode)).isoformat()
    tags = ', '.join([f"\"{tag}\"" for tag in [station, show, airyear]])
    content = template.substitute(
        name=name,
        isodate=isodate,
        tags=tags,
        season=season,
        year=airyear,
        episode=episode,
        filename=target,
        show=show,
        longdate=airdate,
        stationdesc=airloc,
        spinlink=link,
    )
    season_dir = f"content/posts/s{season}"
    filename = f"content/posts/s{season}/e{episode}.md"
    if not os.path.isdir(season_dir):
        os.mkdir(season_dir)
    with open(filename, "w") as md:
        md.write(content)
