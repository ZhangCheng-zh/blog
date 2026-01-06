"""
Description

Your task is to write a function that converts a non-negative integer into its spoken word (English) equivalent.

Examples
fn(7)      => "seven"
fn(77)     => "seventy-seven"
fn(777)    => "seven hundred and seventy-seven"
fn(7777)   => "seven thousand seven hundred and seventy-seven"
fn(54321)  => "fifty-four thousand three hundred and twenty-one"

Rules & Notes

Numbers should be written in British English style, using:

hyphens for compound numbers (twenty-one, seventy-seven)

the word "and" between hundreds and tens/ones
(e.g. "three hundred and five")

Scale words include:

hundred

thousand

(and potentially higher if extended)

No trailing or leading spaces.

Output should be a single string.
"""

def numberToWords(n):
    if n == 0:
        return 'zero'
    
    under_20 = [
        "", "one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"
    ]

    tens = [
        "", "", "twenty", "thirty", "forty", "fifty",
        "sixty", "seventy", "eighty", "ninety"
    ]

    def twoDigits(num):
        if num < 20:
            return under_20[num]
        t, r = divmod(num, 10)
        return tens[t] + (f"-{under_20[r]}" if r else '')

    def threeDigits(num):
        h, r = divmod(num, 100)
        if h == 0:
            return twoDigits(r)
        if r == 0:
            return under_20[h] + 'hundred'
        return under_20[h] + ' hundred and ' + twoDigits(r)
    
    parts = []
    thousands, rest = divmod(n, 1000)

    if thousands:
        parts.append(threeDigits(thousands) + " thousand") 
    if rest:
        parts.append(threeDigits(rest))

    return ' '.join(parts)

print(numberToWords(7))      # "seven"
print(numberToWords(77))     # "seventy-seven"
print(numberToWords(777))    # "seven hundred and seventy-seven"
print(numberToWords(7777))   # "seven thousand seven hundred and seventy-seven"
print(numberToWords(54321))  # "fifty-four thousand three hundred and twenty-one"