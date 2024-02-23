#!/usr/bin/python3

# https://stackoverflow.com/a/39596504

def ordinal(integer):
    # The suffix list
    suffix_list = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']

    if integer % 100 in (11, 12, 13):
        s = 'th'
    else:
        s = suffix_list[integer % 10]

    return str(integer) + s
