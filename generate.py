import datetime
import os

from string import Template

MUSIC_HOST_URL = "https://tin-radio-files.storage.googleapis.com/"

POST_TEMPLATE = Template("""+++
title = "${name}"
date = ${isodate}
tags = [${tags}]
seasons = ["Season ${season}"]
seasons_weight = ${episode}
+++

{{% audio src="${baseurl}${filepath}" %}}

${show} on ${longdate}

Aired on ${stationdesc}

Playlist/Spinitron: ${spinlink}
""")


def date_th(day):
    end = "th"
    if day % 10 == 1:
        end = "st"
    elif day % 10 == 2:
        end = "nd"
    return str(day) + end


def loc_str(station):
    if station == "WVUD":
        return "91.3 WVUD: The Voice of the University of Delaware"
    if station == "The Basement":
        return "91.3 WVUD HD-2: The Basement U of D Student Radio"
    raise ValueError(f"Unknown station: {station}")


def extract(names_file, data_file):
    with open(names_file, "r") as file:
        titles = file.readlines()
    with open(data_file, "r") as file:
        data = file.readlines()
    return titles, data


def file_from_title(title):
    title = title.lower()
    title = title.replace(" ", "_")
    title = title.replace("(", "")
    title = title.replace(")", "")
    title = title.replace("'", "_")
    return title + ".mp3"


def generate(names_file, data_file):
    titles, data = extract(names_file, data_file)
    for i in range(len(titles)):
        title = titles[i].strip()
        datum = data[i].strip()
        station, show, date, link = datum.split(';')
        rawdate = datetime.datetime.fromisoformat(date)
        day = date_th(rawdate.day.real)
        airdate = rawdate.strftime(f"%A, %B {day}, %Y")
        airyear = rawdate.strftime("%Y")
        airloc = loc_str(station)
        filepath = file_from_title(title)
        parts = title.split(" ")
        name = ' '.join(parts[5:]).strip()
        season = int(parts[2][1:])
        episode = int(parts[3][1:])
        isodate = rawdate.isoformat()
        tags = ', '.join([f"\"{tag}\"" for tag in [station, show, airyear]])
        content = POST_TEMPLATE.substitute(
            name=name,
            isodate=isodate,
            tags=tags,
            season=season,
            year=airyear,
            episode=episode,
            baseurl=MUSIC_HOST_URL,
            filepath=filepath,
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


if __name__ == "__main__":
    generate("names.txt", "data.txt")