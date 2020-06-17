"""
@author: mvskoke
@since: 6/17/2020
"""

import sys
import argparse

# parse files and flags at cmdline
parser = argparse.ArgumentParser(description='Converts romanizations/orthographies to IPA, and vice versa. \
                                Converting text can be done through command line input or a separate text file.')

parser.add_argument('romanization', help='.txt file which lists all the romanization > IPA pairs.')

parser.add_argument('--lexicon', help="Optional lexicon file to convert. INCLUDE the '--lexicon' flag before the filename!")

parser.add_argument('-d', '--direction', action='store_true', help='Flips the direction of conversion. \
                    Default direction upon starting the program with no flag(s) is romanization -> IPA.')

parser.add_argument('-o', '--outputf', action='store_true', help='Enables printing the conversion to a file.')
args = parser.parse_args()


""" GLOBAL VARIABLES """
# two boolean values are set by the cmdline flags
# this one dictates direction of conversion
IPA_TO_ROMZ = args.direction

# allows writing to output file
WRITE_OUTPUT_TO_FILE = args.outputf

FLAGS = {'q', '-o', '-d', '-od', '-do', '--direction', '--outputf',
         '--direction --outputf', '--outputf --direction'}

"""
store tuples of (romanization, ipa) in a list
use ordered structure in order to allow allophony
or more complex romanization rules
"""
CONVERSIONS = []


""" MAIN PROGRAM FUNCTIONS """
def parse_romanization(romanization_file):
    """Read in a romanization file and parse it"""
    global CONVERSIONS
    CONVERSIONS = []

    try:
        with open(romanization_file, 'r', encoding='utf8') as f:
            for line in f.readlines():
                # allow comments
                if ';' == line[0]:
                    continue
                # in case user has empty lines or lines with random whitespace
                elif line.strip() == '':
                    continue

                line = line.split('>')

                # we use '#' as the whitespace placeholder
                char = line[0].strip().replace('#', ' ')
                ipa = line[1].strip().replace('#', ' ')
                CONVERSIONS.append((char, ipa))

    except FileNotFoundError:
        print(f"ERROR: Failed to locate romanization file '{romanization_file}'")
        sys.exit()
        
    except IndexError:
        print(f"ERROR: Failed to parse romanization file '{romanization_file}'")
        sys.exit()

    print(f"ROMANIZATION FILE '{romanization_file}' SUCCESSFULLY PARSED.")


def toggle_flag(flag):
    """Retroactively toggle flags during conversion"""
    global IPA_TO_ROMZ
    global WRITE_OUTPUT_TO_FILE

    if flag == 'q':
        print("\n\n\nThanks for using the IPA converter!\n--mvskoke 2020\n")
        sys.exit()
    # two flags
    elif flag in {'-od', '-do', '--direction --outputf', '--outputf --direction'}:
        IPA_TO_ROMZ = not IPA_TO_ROMZ
        WRITE_OUTPUT_TO_FILE = not WRITE_OUTPUT_TO_FILE
    # only one flag
    elif flag == '-d' or flag == '--direction':
        IPA_TO_ROMZ = not IPA_TO_ROMZ
    elif flag == '-o' or flag == '--outputf':
        WRITE_OUTPUT_TO_FILE = not WRITE_OUTPUT_TO_FILE

    """
    this toggle_flag function only gets called in the loop,
    which only happens if the argument is in FLAGS.
    MEANING: THIS FUNCTION ALLOWS US to ONLY print these
    update messages if user actually updated a flag!!!
    """
    if WRITE_OUTPUT_TO_FILE:
        print("WRITE OUT CONVERSION TO NEW FILE: TOGGLED <ON>.")
    else:
        print("WRITE OUT CONVERSION TO NEW FILE: TOGGLED <OFF>.")

    if IPA_TO_ROMZ:
        print("CONVERSION MODE: IPA > ROMANIZATION")
    else:
        print("CONVERSION MODE: ROMANIZATION > IPA")


def convert_words(input_lexicon):
    """Converts any string passed in"""
    for char_ipa_pair in CONVERSIONS:
        char = char_ipa_pair[0]
        ipa = char_ipa_pair[1]

        if char == ipa:
            # prevents unnecessary searching and replacing
            continue
        elif char in input_lexicon and not IPA_TO_ROMZ:
            input_lexicon = input_lexicon.replace(char, ipa)
        elif ipa in input_lexicon and IPA_TO_ROMZ:
            input_lexicon = input_lexicon.replace(ipa, char)

    """
    call .lower() here; better to call it here once,
    rather than everytime you convert something above.
    also allows conversion from case-sensitive romanizations;
    if romanization had upper- and lowercase, and since python's
    replace method knows to match case, the resulting IPA
    would have uppercase letters.
    """
    if not IPA_TO_ROMZ:
        input_lexicon = input_lexicon.lower()

    return input_lexicon


def write_output_to_file(output_lexicon):
    """Prints a conversion to a new file"""
    outputf_name = input('\nTYPE OUTPUT FILE NAME (INCLUDE FILE EXTENSION):\n>>> ')

    # error-handle bad filenames
    while True:
        if outputf_name == 'q':
            print("\nOUTPUT FILE CANCELLED.\n\n\n\nThanks for using the IPA converter! \
                  \n--mvskoke 2020\n")
            sys.exit()

        try:
            with open(outputf_name, 'w', encoding='utf8') as f:
                f.write(output_lexicon)
        except OSError:
            print(f"\nERROR: INVALID FILE NAME: {outputf_name}")
            outputf_name = input('TYPE OUTPUT FILE NAME (INCLUDE FILE EXTENSION):\n>>> ')
        else:
            break

    # also prints new file name for the user to see
    print(f"\n =============== {outputf_name} =============== \
            \n{output_lexicon}")


"""The next two functions are this program's main functionality"""
def convert_lexfile():
    """Read in and convert txtfiles"""
    lexfile = args.lexicon

    while True:
        try:
            with open(lexfile, 'r', encoding='utf8') as f:
                lexicon_words = f.read()
                converted_words = convert_words(lexicon_words)

            # --outputf; writes conversion to output file
            if WRITE_OUTPUT_TO_FILE:
                write_output_to_file(converted_words)
            else:
                print(f"\n =============== {lexfile} =============== \
                        \n{converted_words}")

        except FileNotFoundError:
            print(f"\nERROR: No such file '{lexfile}' found.")

        """
        DO NOT PUT THE NEXT LINE OF CODE IN A 'finally:' BLOCK!!!!!
        when the previous if-else statement used to be inside
        the try block, and this line was in a finally block, 
        it prevented users from quitting with 'q' when asked 
        to input outputf_name
         - probably could've used an 'else:' block...

        anyways, get next lexicon file to convert
        """
        lexfile = input("\nNEXT FILE:\n>>> ").strip()

        """
        CHECK FOR RETROACTIVE FLAG TOGGLE
        loop allows constant toggling/retoggling 
        of flags and changing romanization files
        """
        while lexfile in FLAGS or lexfile[:2] == '-r':
            # now check if lexfile is only in FLAGS
            if lexfile in FLAGS:
                toggle_flag(lexfile)
                lexfile = input("\nNEXT FILE:\n>>> ").strip()
            
            # CHECK FOR RETROACTIVE ROMANIZATION FILE CHANGE
            # file extension required; loop already checked for flag
            elif lexfile[-4:] == '.txt':
                parse_romanization(lexfile[2:].strip())
                lexfile = input("\nNEXT FILE:\n>>> ").strip()


def convert_cmdline():
    """Read in and convert text thru command line"""
    while True:
        lex = input('\n>>> ').strip()

        # check for flags or romanization file changes
        while lex in FLAGS or lex[:2] == '-r':
            if lex in FLAGS:
                toggle_flag(lex)
                lex = input("\n>>> ").strip()
            elif lex[-4:] == '.txt':
                parse_romanization(lex[2:].strip())
                lex = input("\n>>> ").strip()

        converted_words = convert_words(lex)

        # --outputf; write out to output file if user toggled that flag
        if WRITE_OUTPUT_TO_FILE:
            write_output_to_file(converted_words)
        else:
            print(f'>>> {converted_words}')


if __name__ == '__main__':
    print('\n\n')
    parse_romanization(args.romanization)

    # upon startup, remind user of their flag settings; more user-friendly
    if WRITE_OUTPUT_TO_FILE:
        print("\nWRITE OUT CONVERSION TO NEW FILE: TOGGLED <ON>.")
    else:
        print("\nWRITE OUT CONVERSION TO NEW FILE: TOGGLED <OFF>.")
    if IPA_TO_ROMZ:
        print("CONVERSION MODE: IPA > ROMANIZATION")
    else:
        print("CONVERSION MODE: ROMANIZATION > IPA")

    # begin main program
    if '--lexicon' in sys.argv:
        convert_lexfile()
    else:
        convert_cmdline()