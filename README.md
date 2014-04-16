Renoise LUA script.

To be loaded inside renoise (v.2.8 tested) as a tool. Simply dragging and dropping the '.xrnx' folder inside Renoise will do.

It will send the current position of the song via a MIDI SongPos message every time the current position changes.

The script attaches to the idle_handler, so it may be not precise timming performant. (Called every 10ms)

Calculations are done based on a 64 pattern length. This can be changed inside the script.

no3productionz@gmail.com
@deblockgame
