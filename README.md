# DRT #
DRT is a command line based DVD copying and ripping management program. It requires
[dvdbackup](http://dvdbackup.sourceforge.net/) to copy the DVD to disc and [HandBrakeCLI](https://handbrake.fr/) to
transcode the video.

DRT is optimised for TV series based DVD ripping.

## dvdcopy ##
A small python program that uses dvdbackup to copy the DVD to your hard disc.

If you make it the default program for opening DVDs then it is fully automatic.

## dvdprocess ##
dvdprocess allows you to set a title for the video files, with automatic series and episode numbering.

```
Usage:
    dvdprocess --help
    dvdprocess --version
    dvdprocess --allsaved
    dvdprocess -A
    dvdprocess --listsaved
    dvdprocess -l
    dvdprocess --incoming
    dvdprocess -r
    dvdprocess --saved SAVEDNAME ...
    dvdprocess -s SAVEDNAME ...
    dvdprocess --first
    dvdprocess -S

Options:
    -A --allsaved           process all saved DVDs.
    -h --help               this help message.
    -l --listsaved          list all saved DVDs and exit.
    -r --incoming           read the incoming dir. and build the DVD tree for editing.
    -s --saved SAVEDNAME    process the saved DVD for SAVEDNAME, can be repeated.
    -S --first              process the first saved DVD and exit.
    --version               version info.

Notes:
    Process module of drt application

    Reads a copied dvd directory.
    Produces an info file.
    Allows user to name the dvd and assign episode numbers and names to the tracks.
    Allows user to select which tracks to process.
    Allows user to toggle the burning in of subtitles.
    Allows user to save the edited data for later processing.
```
