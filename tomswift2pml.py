import linecache


"""
replace -- with \a150\a150
"""

# lifted from a stackoverflow snippet and modified by me.
def int_to_roman(input):
    """ Convert an integer to a Roman numeral. """
    if not isinstance(input, type(1)):
        raise TypeError(f"expected integer, got {type(input)}")

    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 3999")

    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')

    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count

    return ''.join(result)

def gutenberg2pml(in_file, out_file):
    out_file = "Tom_Swift_and_His_Airship.pml"
    ow = open(out_file, "w")

    book_title = linecache.getline(in_file, 1).split("Title: ")[1].rstrip('\n')
    year = linecache.getline(in_file, 2).split("Copyright: ")[1].rstrip('\n')

    print(f"""\\v
TITLE="{book_title}"
AUTHOR="Victor Appleton"
PUBLISHER="Grosset & Dunlap"
COPYRIGHT="{year}"
EISBN=""
\\v
\\m="cover.png"
\p
\\c\\l\\B{book_title}\\B\\l

\\sBy Victor Appleton\s
\\c
\\w="100%"
    
    
    
    
\\c\\s\\i {year} \\i\\s
\\c\\n""", file=ow)

    with open(in_file, 'r') as fp:
        # start at 4 to skip over the metadata lines
        paragraph = []

        for line_no, line in enumerate(fp, start=1):
            # print(line_no, line)

            """
            can skip with this, too:
            ----
            from itertools import islice
    
            lines = list("abcdefghij")
            
            lit = iter(enumerate(lines))
            for iline, line in lit:
                print(iline, line)
                if line == "c":
                    # skip 3
                    next(islice(lit, 3,3), None)
            """
            if line.startswith("Title:") or line.startswith("Copyright:"):
                continue

            if line.startswith("Chapter"):
                # format the chapter title
                chapter_number = line.split("Chapter ")[1].rstrip("\n")
                # title is 2 lines ahead of this one
                chapter_title = linecache.getline(in_file, line_no + 2).rstrip("\n")
                # print(f"chapter line no={line_no} & chapter name={line_no + 2}: {chapter_title}")
                print(f"""\\x
\\c\\B\\l Chapter {int_to_roman(int(chapter_number))}: \\l\\B

\\l\\u{chapter_title}\\l\\u
\\c
\\x\\n""", file=ow)
            else:
                if not line.isspace() and line.rstrip('\n') != chapter_title:
                    paragraph.append(line.rstrip('\n'))

                """
                # this causes the last paragraph to never print because there is no blank line after it...
                the source file must be terminated with two blank lines, i.e. a full line whose only content is "\n" 
                """
                if line.isspace():
                # a blank line delimits paragraphs
                    joined_paragraph = f"{' '.join(paragraph)}\n"
                    if not joined_paragraph.isspace():
                        print(joined_paragraph, file=ow)

                    # TODO make a paragraph counter?
                    paragraph.clear()

        fp.close()

    print("""


\w="30%"
\c\BTHE END\B
\c
""", file=ow)

    ow.close()


if "__name__" == "__main__":
    in_file = input("Enter text file name")
    # TODO check for txt?
    out_file = f"{in_file.split('.')[0]}.pml"

    gutenberg2pml(in_file, out_file)
