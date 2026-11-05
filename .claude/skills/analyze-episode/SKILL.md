---
name: analyze-episode
description: Check the sequence of states, actions, and rewards. Identify any loops, dead ends, or other issues in the episode. Return a summary of the episode analysis.
---
If the episode contains loops, return "loop detected". If the episode contains dead ends, return "dead end detected". If the episode is valid and no loops or dead ends are detected, return "episode valid".