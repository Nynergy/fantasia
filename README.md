# fantasia

A TUI for editing ID3v2 tags on mp3 files

------------------------------------------------------------------------------

## What is fantasia and why does it exist?

_fantasia_ is a terminal user interface application for adding, removing, and
modifying ID3v2 tags for mp3 files. For an explanation of ID3 tags, see [this
article](https://en.wikipedia.org/wiki/ID3).

As with all the apps I use, I started using a graphical tag editor (in this case
[picard](https://picard.musicbrainz.org/)), and have now found that I want to
use a terminal interface instead. So I wrote my own, because that's what I like
to do. You can use it too, if you want.

## What exactly does it do?

At the moment, it just renders a dummy panel to the terminal. Have fun.

## How can I run it?

First, you need to have the proper dependencies installed. This program utilizes
ncurses, and in the future it will use [eyed3](https://eyed3.readthedocs.io/en/latest/)
for editing tags. Make sure you have these installed before using _fantasia_.

Once dependencies are installed, run it using `./fantasia`

## How can I configure it?

For right now, configuration is done in the `config.json` file. See the config
file provided in the repository for how to customize it.

## How do I use it?

Here are the commands that exist right now:

Key | Action
----|-------
<kbd>q</kbd> | quit fantasia
