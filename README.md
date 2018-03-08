# DRT #
DRT is a command line based DVD copying and ripping management program. It requires
[dvdbackup](http://dvdbackup.sourceforge.net/) to copy the DVD to disc and [HandBrakeCLI](https://handbrake.fr/) to
transcode the video.

It allows you to setup transcoding of your DVD with meaningful track names for later processing when your computer is
idle.

DRT is optimised for TV series based DVD ripping.

There is a config file at `~/.config/drt.yaml`.

## Installing ##
This is still in beta, if you want to test it use a virtualenv and a reasonably new version of python3, vis:

```
# debian based distros (ubuntu etc).
mkdir drt
cd drt
mkvirtualenv --system-site-packages --python=/usr/bin/python3 drt
pip install drt
dvdprocess -v
```

You'll need to create a configuration file at `$HOME/.config/drt.yaml`

```
# $HOME/.config/drt.yaml
device: /dev/sr0
rootdir: ~/Videos/dvd
dvdoutput: ~/Videos/dvd/output
outputdir: ~/Videos/dvd/incoming
tmpdir: ~/Videos/dvd/bare
completeddir: ~/Videos/dvd/processed
saveddir: ~/Videos/dvd/saved
handbrake: /usr/bin/HandBrakeCLI
dvdbackup: /usr/bin/dvdbackup
eject: /usr/bin/eject
shorttrack: 300
```
only the keys `device`, `rootdir`, `handbrake`, `dvdbackup` and `shorttrack` are required, the rest are inferred.

## dvdcopy ##
A small python program that uses dvdbackup to copy the DVD to your hard disc.
When run, it asks for a name for the DVD.  This is how it will be known to `dvdprocess`.

## dvdprocess ##
dvdprocess allows you to set a title for the video files, with automatic series and episode numbering.
The Series/Episode tag can be removed by setting the Series number to -1.
```
dvdprocess command module.

part of the drt package.

Usage:
    dvdprocess
    dvdprocess --help
    dvdprocess -v
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
    -r --incoming           read the incoming dir. and build the DVD tree for editing. Default action
                            if no options supplied.
    -s --saved SAVEDNAME    process the saved DVD for SAVEDNAME, can be repeated.
    -S --first              process the first saved DVD and exit.
    -v --version            version info.

Notes:
    Process module of drt application

    dvdprocess on it's own will read the incoming directory and start the naming process.

    Reads a copied dvd directory.
    Produces an info file.
    Allows user to name the dvd and assign episode numbers and names to the tracks.
    Allows user to select which tracks to process.
    Allows user to toggle the burning in of subtitles.
    Allows user to save the edited data for processing at a later time.
```

### Example ###
After copying 2 DVDs I have 2 folders in my incoming directory:

```
$ ls ~/Videos/dvd/incoming
jjds2d2  SPIRAL_S2_D2
```

Running `dvdprocess` I'm presented with the following (short tracks, less than 5 minutes are not shown):

```
$ ./dvdprocess -r
DVD: jjds2d2
Series Name: jjds2d2
Series ID: 1
Start Episode: 1
  +   2 - jjds2d2 2 - 02:59:11 - 10751 - English/English
  +   3 - jjds2d2 3 - 01:29:29 - 5369 - English/English
  +   4 - jjds2d2 4 - 01:29:42 - 5382 - English/English
edit [d]vd, edit [t]racks, [s]ave, s[k]ip, [o]k (o) >
```
the menu allows me to edit the DVD name, series number and starting episode number
```
edit [d]vd, edit [t]racks, [s]ave, s[k]ip, [o]k (o) > d
Series Name (jjds2d2) > Judge John Deed
Series number (1) > 2
Starting Episode Number (1) > 3
DVD: jjds2d2
Series Name: Judge John Deed
Series ID: 2
Start Episode: 3
  +   2 - Judge John Deed S02E03 - 02:59:11 - 10751 - English/English
  +   3 - Judge John Deed S02E04 - 01:29:29 - 5369 - English/English
  +   4 - Judge John Deed S02E05 - 01:29:42 - 5382 - English/English
```
which, as you can see has changed the name of each track, giving it series and episode numbers.
Editing the track menu allows me to add track titles and select which tracks are to be processed.
```
edit [d]vd, edit [t]racks, [s]ave, s[k]ip, [o]k (o) > t
  +   2 - Judge John Deed S02E03 - 02:59:11 - 10751 - English/English
  +   3 - Judge John Deed S02E04 - 01:29:29 - 5369 - English/English
  +   4 - Judge John Deed S02E05 - 01:29:42 - 5382 - English/English
```
Now I select the track naming option:
```
edit (s)elected tracks, edit (b)urnin subtitles, edit track (n)ames () > n
  +   2 - Judge John Deed S02E03 - 02:59:11 - 10751 - English/English
  +   3 - Judge John Deed S02E04 - 01:29:29 - 5369 - English/English
  +   4 - Judge John Deed S02E05 - 01:29:42 - 5382 - English/English
Select track number or (e)xit track editor. () > 3
Track 3 title: () > Nobody's Fool
  +   2 - Judge John Deed S02E03 - 02:59:11 - 10751 - English/English
  +   3 - Judge John Deed S02E04 - 01:29:29 - 5369 - English/English Nobody's Fool
  +   4 - Judge John Deed S02E05 - 01:29:42 - 5382 - English/English
Select track number or (e)xit track editor. () > 4
Track 4 title: () > Everyone's Child
  +   2 - Judge John Deed S02E03 - 02:59:11 - 10751 - English/English
  +   3 - Judge John Deed S02E04 - 01:29:29 - 5369 - English/English Nobody's Fool
  +   4 - Judge John Deed S02E05 - 01:29:42 - 5382 - English/English Everyone's Child
Select track number or (e)xit track editor. () > e
DVD: jjds2d2
Series Name: Judge John Deed
Series ID: 2
Start Episode: 3
  +   2 - Judge John Deed S02E03 - 02:59:11 - 10751 - English/English
  +   3 - Judge John Deed S02E04 - 01:29:29 - 5369 - English/English Nobody's Fool
  +   4 - Judge John Deed S02E05 - 01:29:42 - 5382 - English/English Everyone's Child
```
track selection:
```
edit [d]vd, edit [t]racks, [s]ave, s[k]ip, [o]k (o) > t
  +   2 - Judge John Deed S02E03 - 02:59:11 - 10751 - English/English
  +   3 - Judge John Deed S02E04 - 01:29:29 - 5369 - English/English Nobody's Fool
  +   4 - Judge John Deed S02E05 - 01:29:42 - 5382 - English/English Everyone's Child
edit (s)elected tracks, edit (b)urnin subtitles, edit track (n)ames () > s
Tracks to process ([2, 3, 4]) > 3 4
DVD: jjds2d2
Series Name: Judge John Deed
Series ID: 2
Start Episode: 3
      2 - jjds2d2 2 - 02:59:11 - 10751 - English/English
  +   3 - Judge John Deed S02E03 - 01:29:29 - 5369 - English/English Nobody's Fool
  +   4 - Judge John Deed S02E04 - 01:29:42 - 5382 - English/English Everyone's Child
```
As you can see by de-selecting track 2 the remaining tracks are re-numbered accordingly.
I then saved the information for processing later. `dvdprocess` then moves onto the next DVD in the directory.
```
edit [d]vd, edit [t]racks, [s]ave, s[k]ip, [o]k (o) > s
DVD: SPIRAL_S2_D2
Series Name: SPIRAL_S2_D2
Series ID: 1
Start Episode: 1
  + b 1 - SPIRAL_S2_D2 1 - 03:30:17 - 12617 - Francais/English
  + b 2 - SPIRAL_S2_D2 2 - 00:50:36 - 3036 - Francais/English
  + b 3 - SPIRAL_S2_D2 3 - 00:55:07 - 3307 - Francais/English
  + b 4 - SPIRAL_S2_D2 4 - 00:52:23 - 3143 - Francais/English
  + b 6 - SPIRAL_S2_D2 6 - 00:52:11 - 3131 - Francais/English
      7 - SPIRAL_S2_D2 7 - 00:00:48 - 48 - none/none
```
The `b` next to the selected track shows that `dvdprocess` has detected that the main audio track and the first
sub-title track have different languages (Francais/English in this case).  It has automatically selected to burn the
subtitles onto the video track.  This can be turned off in the track editor.
```
edit [d]vd, edit [t]racks, [s]ave, s[k]ip, [o]k (o) > t
  + b 1 - SPIRAL_S2_D2 1 - 03:30:17 - 12617 - Francais/English
  + b 2 - SPIRAL_S2_D2 2 - 00:50:36 - 3036 - Francais/English
  + b 3 - SPIRAL_S2_D2 3 - 00:55:07 - 3307 - Francais/English
  + b 4 - SPIRAL_S2_D2 4 - 00:52:23 - 3143 - Francais/English
  + b 6 - SPIRAL_S2_D2 6 - 00:52:11 - 3131 - Francais/English
      7 - SPIRAL_S2_D2 7 - 00:00:48 - 48 - none/none
edit (s)elected tracks, edit (b)urnin subtitles, edit track (n)ames () > b
  + b 1 - SPIRAL_S2_D2 1 - 03:30:17 - 12617 - Francais/English
  + b 2 - SPIRAL_S2_D2 2 - 00:50:36 - 3036 - Francais/English
  + b 3 - SPIRAL_S2_D2 3 - 00:55:07 - 3307 - Francais/English
  + b 4 - SPIRAL_S2_D2 4 - 00:52:23 - 3143 - Francais/English
  + b 6 - SPIRAL_S2_D2 6 - 00:52:11 - 3131 - Francais/English
      7 - SPIRAL_S2_D2 7 - 00:00:48 - 48 - none/none
Toggle Burnin (Track Num or (A)ll) () > 1
DVD: SPIRAL_S2_D2
Series Name: SPIRAL_S2_D2
Series ID: 1
Start Episode: 1
  +   1 - SPIRAL_S2_D2 1 - 03:30:17 - 12617 - Francais/English
  + b 2 - SPIRAL_S2_D2 2 - 00:50:36 - 3036 - Francais/English
  + b 3 - SPIRAL_S2_D2 3 - 00:55:07 - 3307 - Francais/English
  + b 4 - SPIRAL_S2_D2 4 - 00:52:23 - 3143 - Francais/English
  + b 6 - SPIRAL_S2_D2 6 - 00:52:11 - 3131 - Francais/English
      7 - SPIRAL_S2_D2 7 - 00:00:48 - 48 - none/none
```
The rest of the process is the same as for the first DVD.
