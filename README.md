# GENETIS-RHINO

## Developer notes

### Linter

We automatically run a linter on newly commited code. It's job is to yell at us if we don't follow good Python programming conventions so that we can fix problems instead of getting tripped up by them later. If it yells at you, usually the message it gives will be self explanatory. If it's ever not self-explanatory, take a look at the ID of the rule that was violated and search for it here: https://docs.astral.sh/ruff/rules/

<img width="586" height="221" alt="image" src="https://github.com/user-attachments/assets/db39ac3f-46c2-42ee-9b70-590327fd84be" />

Importantly, the linter requires that you [specify types for your variables](https://docs.python.org/3/library/typing.html) and [use docstrings](https://www.geeksforgeeks.org/python/python-docstrings/).

If the linter yells at you for something that you disagree with, we can talk about changing the rules.
