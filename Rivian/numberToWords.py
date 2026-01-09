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
class Solution:
    # 1 to 9 billion
    def integer_to_word(self, num):
        specials = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(" ")
        tens = "twenty thirty forty fifty sixty seventy eighty ninety".split(" ")
        hundred = "hundred"
        thousand = "thousand"
        million = "million"
        billion = "billion"

        if num < 20:
            return specials[num]
        if num < 100:
            if num % 10 == 0:
                return tens[num // 10 - 2]
            return tens[num // 10 - 2] + "-" + self.integer_to_word(num % 10)
        if num < 1000:
            if num % 100 == 0:
                return self.integer_to_word(num // 100) + " " + hundred
            return  self.integer_to_word(num // 100) + " " + hundred + " and " + self.integer_to_word(num % 100)
        if num < 1000000:
            if num % 1000 == 0:
                return self.integer_to_word(num // 1000) + " " + thousand
            return  self.integer_to_word(num // 1000) + " " + thousand + " " + self.integer_to_word(num % 1000)
        if num < 1000000000:
            if num % 1000000 == 0:
                return self.integer_to_word(num // 1000000) + " " + million
            return  self.integer_to_word(num // 1000000) + " " + million + " " + self.integer_to_word(num % 1000000)


print(numberToWords(7))      # "seven"
print(numberToWords(77))     # "seventy-seven"
print(numberToWords(777))    # "seven hundred and seventy-seven"
print(numberToWords(7777))   # "seven thousand seven hundred and seventy-seven"
print(numberToWords(54321))  # "fifty-four thousand three hundred and twenty-one"