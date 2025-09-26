# GENETIS-RHINO

[![CI](https://github.com/osu-particle-astrophysics/GENETIS-RHINO/actions/workflows/ci.yml/badge.svg)](https://github.com/osu-particle-astrophysics/GENETIS-RHINO/actions/workflows/ci.yml)

## Developer notes

### Linter

We automatically run a linter on newly commited code. Its job is to yell at 
us if we don't follow good Python programming conventions so that we can fix problems instead of getting tripped up by them later. If it yells at you, usually the message it gives will be self-explanatory. If it's ever not self-explanatory, take a look at the ID of the rule that was violated and search for it here: https://docs.astral.sh/ruff/rules/

<img width="586" height="221" alt="image" src="https://github.com/user-attachments/assets/db39ac3f-46c2-42ee-9b70-590327fd84be" />

Importantly, the linter requires that you [specify types for your variables](https://docs.python.org/3/library/typing.html) and [use docstrings](https://www.geeksforgeeks.org/python/python-docstrings/).

If the linter yells at you for something that you disagree with, we can talk about changing the rules.

### Testing

We have continuous integration testing setup using pytest. Please write tests for all code you contribute. Tests should go in the `tests` direction in a file that starts with `test_`. Each test function name should also start with `test_`.

### Adding code

Please add code by:
1. Creating a separate branch
2. Adding your code to that branch
3. Pushing the branch
4. Opening a pull request
5. Verifying that all checks pass
6. Merging

This will ensure that code only gets added if it passes all tests
