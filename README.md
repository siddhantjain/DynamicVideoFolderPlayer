# DynamicVideoFolderPlayer


This is small script I wrote for solving the following problem:

Given a folder with a set of videos, play all videos in the folder. If a new video is added to the folder, that should be enqueued to be played. However, if all videos have been played once and we are looping through the videos, the addition of a new video should kill the existing loop and start playing the new video(s).

Writing in Python and uses VLC. There are some VLC settings that need to be set for this to work well.

## VLC Settings

Set VLC to single instance only. Also check the box to enqueue files when there are mutliple instances of VLC opened.
Finally, set VLC to close itself on end of playlist


## Before you run the script
For this script I am using a python package called psutils. You will have to added that package to run this script.
TBD: Add link to psutils

## Usage

Simply run the python file. As of now, everything is hardcoded. Look at the constants, to make changes for the script to run locally for you.




