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

# 1 to 9 billion
# def numberToWords(num):
#     specials = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(" ")
#     tens = "twenty thirty forty fifty sixty seventy eighty ninety".split(" ")
#     hundred = "hundred"
#     thousand = "thousand"
#     million = "million"
#     billion = "billion"

#     if num < 20:
#         return specials[num]
#     if num < 100:
#         if num % 10 == 0:
#             return tens[num // 10 - 2]
#         return tens[num // 10 - 2] + "-" + numberToWords(num % 10)
#     if num < 1000:
#         if num % 100 == 0:
#             return numberToWords(num // 100) + " " + hundred
#         return  numberToWords(num // 100) + " " + hundred + " and " + numberToWords(num % 100)
#     if num < 1000000:
#         if num % 1000 == 0:
#             return numberToWords(num // 1000) + " " + thousand
#         return  numberToWords(num // 1000) + " " + thousand + " " + numberToWords(num % 1000)
#     if num < 1000000000:
#         if num % 1000000 == 0:
#             return numberToWords(num // 1000000) + " " + million
#         return  numberToWords(num // 1000000) + " " + million + " " + numberToWords(num % 1000000)

def numberToWords(num):
    specials = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(" ")
    tens = 'twenty thirty forty fifty sixty seventy eighty ninety'.split(' ')
    hundred = 'hundred'
    thousand = 'thousand'
    million = 'million'
    billion = 'billion'
    if num == 0:
        return 'zero'

    if num < 20: # [0, 20)
        return specials[num]
    if num < 100: # [20, 100)
        if num % 10 == 0:
            return tens[(num // 10) - 2]
        return tens[(num // 10) - 2] + '-' + numberToWords(num % 10)
    if num < 1000: # [100, 1000)
        if num % 100 == 0:
            return numberToWords(num // 100) + ' ' + hundred
        return numberToWords(num // 100) + ' ' + hundred + ' and ' + numberToWords(num % 100)
    if num < 1000000: # [1000, 1 million)
        if num % 1000 == 0:
            return numberToWords(num // 1000) + ' ' + thousand
        return numberToWords(num // 1000) + ' ' + thousand + ' and ' + numberToWords(num % 1000)
    if num < 1000000000: #[1 million, 1 billion)
        if num % 1000000 == 0:
            return numberToWords(num // 1000000) + ' ' + million
        return numberToWords(num // 1000000) + ' ' + million + ' and ' + numberToWords(num % 1000000)

    if num % 1000000000 == 0:
        return numberToWords(num // 1000000000) + ' ' + billion
    return numberToWords(num // 1000000000) + ' ' + billion + ' and ' + numberToWords(num % 1000000000)


def runTests():
    # 0 / small
    assert numberToWords(0) == "zero"
    assert numberToWords(7) == "seven"
    assert numberToWords(19) == "nineteen"
    assert numberToWords(20) == "twenty"
    assert numberToWords(21) == "twenty-one"
    assert numberToWords(90) == "ninety"
    assert numberToWords(99) == "ninety-nine"

    # hundreds
    assert numberToWords(100) == "one hundred"
    assert numberToWords(101) == "one hundred and one"
    assert numberToWords(110) == "one hundred and ten"
    assert numberToWords(115) == "one hundred and fifteen"
    assert numberToWords(999) == "nine hundred and ninety-nine"

    # thousands (multiples / with remainder)
    assert numberToWords(1000) == "one thousand"
    assert numberToWords(1001) == "one thousand and one"
    assert numberToWords(1010) == "one thousand and ten"
    assert numberToWords(1100) == "one thousand and one hundred"
    assert numberToWords(7777) == "seven thousand and seven hundred and seventy-seven"
    assert numberToWords(54321) == "fifty-four thousand and three hundred and twenty-one"

    # millions
    assert numberToWords(1_000_000) == "one million"
    assert numberToWords(1_000_001) == "one million and one"
    assert numberToWords(1_001_000) == "one million and one thousand"
    assert numberToWords(1_234_567) == "one million and two hundred and thirty-four thousand and five hundred and sixty-seven"

    # billions
    assert numberToWords(1_000_000_000) == "one billion"
    assert numberToWords(1_000_000_001) == "one billion and one"
    assert numberToWords(1_000_001_000) == "one billion and one thousand"
    assert numberToWords(2_147_483_647) == (
        "two billion and one hundred and forty-seven million and "
        "four hundred and eighty-three thousand and six hundred and forty-seven"
    )

    print("All tests passed!")

runTests()
