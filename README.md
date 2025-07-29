This is an A* visualization made in pygame. The goal is to generate different paths for the same START and END, where each new path will avoid nodes already used by previous generations, for safety.
Creating safer routes, once conflicts are minimized, would improve real cases where multiple vehicles will do the same trajectory. This is made by adding weights for already used nodes and so the A* can be re-runed.
As a bonus, nodes near walls and dangerous areas have its own weights, so the A* avoids those paths too.

This is not original ideas and is free for anyone to use and improve.
