My notes for the post (my own words):
- spent 3 weekends rewriting my game's save system. not fun. first version just dumped the whole world state to json. 40mb saves lol
- players on steam deck complained saves took like 8 seconds
- new version: only save what changed since the level loaded. saves are under 1mb now and basically instant
- lesson: i should have thought about saves on day one, not month six. retrofitting is miserable
- point of the post: if you're making a game with a big world, design your save format early
