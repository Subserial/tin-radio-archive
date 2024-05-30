# Tin Radio Archive

Get it online at [tinradio.online](https://tinradio.online)!

## Building

Requires Hugo, Python, Git, Bash.

`build.sh` generates posts by:
1. Filling out templates using data from `names.txt` and `data.txt`.
2. Applying patches in the `./patches` folder.

Hugo is left to the Github build action, but `hugo` as a final step should work.
