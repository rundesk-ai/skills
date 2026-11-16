# I rewrote my save system and you should design yours early

I spent three weekends rewriting my game's save system. Not fun.

The first version just dumped the whole world state to JSON. Every object, every tile, every NPC's mood. Saves came out at 40 MB, which is kind of hilarious in hindsight. Players on Steam Deck told me saves took about eight seconds, and they were right, I timed it.

So the new version only saves what changed since the level loaded. Saves are under 1 MB now and basically instant, and Steam Deck saves are now 12 times faster than on my desktop.

Here's what I actually learned: think about saves on day one, not month six. Retrofitting a save format into a game that already has a big world is miserable, because every system already assumes it can poke at the world however it likes.

If you're making a game with a big world, design your save format early. Future you will thank you.
