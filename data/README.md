# Data
csv is used because of the simplicity. More data will be added soon.
## Train
There are now 20000 entries. Some might be in correct before line 1744. It has 50% chance to generate a random board with 5 colours + heal and 50% to generate less than or equal to 5 colours (min 2 colours).

## Test
800 entries, used for testing.

## Small
A very small dataset with 30 entries.

# Refactor
This is a simple script to update from old format. It contains prev, next and score. Now, prev and next are removed and score becomes combo.
