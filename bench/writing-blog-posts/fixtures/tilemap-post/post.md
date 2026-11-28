---
title: "I rewrote my tilemap renderer three times"
draft: true
---

So I rewrote my tilemap renderer three times this month, which is honestly a bit embarrassing, but I think I learned something from it so here we go.

The first version drew every tile every frame. It was fine on my desktop and then I tried it on my old laptop and it ran at like 20fps. Not great. I knew batching was the answer but I kept putting it off because I thought it would be a whole thing.

The second version batched tiles by texture, which got the laptop up to about 55fps. But then I added animated water tiles and the batches kept getting rebuilt every frame, so I was basically back where I started, maybe a little better. I spent two evenings trying to cache the batches before I gave up on that idea completely.

The third version splits the map into 16x16 chunks and only rebuilds a chunk when something in it changes. Water animates with a shader instead of swapping tiles, so the chunks almost never rebuild. The laptop sits at 60fps now and the desktop doesn't even notice.

The lesson, if there is one: I should have measured on the slow machine from day one. I spent most of the month optimizing for the wrong computer lol.
