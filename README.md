# ipa-converter
USAGE: $ python ipa_converter.py romanization.txt [--lexicon input_lexicon.txt] [-o] [--ipa-romz]

The IPA converter will convert romanizations/orthographies to IPA, or vice versa. Unicode supported.
Romanization to IPA is the default mode, but you can indicate otherwise, with the '--ipa-romz' flag.

Additionally the '-o' flag will output a converted lexicon file to a new file. It will still print the
conversion to the terminal if the flag is provided. Do not provide an output file name. You will
provide it during execution.

The first 3 arguments (excluding 'python') must ALWAYS be in the above order. Flags can be in any order.


# ROMANIZATION GUIDELINES
The romanization file should map romanization characters to IPA equivalents, one-to-one,
one per line, in this format: 

    romanization>IPA
    anotherchar>IPA

It may be a simple text file, or a .json file. If using a .txt file, whitespaces will be ignored. .JSON files are
recommended for more complex or detailed romanization schemes.
Comments can be made with semicolon ';'. In-line comments are not possible; all lines with a ';' will beautomatically ignored.
It is recommended that you do not include romanization>IPA pairs if they are equivalent, e.g. /p/ \<p\>.

 - Di/trigraphs and longer are permitted in the romanization characters.
 - Likewise, colons, equal signs, and hyphens are also permitted.
 - However, the right carot \> and semicolon ; are not permitted.


# IMPLEMENTING ALLOPHONY
Allophony can be implemented. In .txt romanization files, the allophonic rules MUST be stated LAST.
Otherwise, allophonic and ordinary rules may bleed into or conflict with each other.


# LEXICON GUIDELINES
An optional input lexicon file may be provided, as a .txt file. If none is provided, then
you may type at the command line and conversions will happen as you go.
But if one IS provided, the resulting conversion will be printed to the terminal.

 - If you choose to type text into the command line for on-the-fly conversion, you will have the ability
to allow the program to continuously read in more text thru standard input until you decide to quit.
 - If you choose to convert a separate lexicon file, you may have the program read in more lexicon files
until you decide to quit. Note that these files MUST be in the same directory as where you save this program.
"Note that unless these files are in the same directroy and where you saved the program, you must specify the directory address.

 - In both the above cases, whether or not you switched conversion modes with the '--ipa-romz' flag,
you may switch modes by entering the same flag. You will be prompted again to enter text or a file.
Entering 'q' will quit the program. (don't do it here)

NOTE: This program is CASE-SENSITIVE. Upper- and lowercase usage in the romanization or lexicon file
will reflect in or change the converted output.

WARNING: Beware of apostrophes! Using ’ and ' in your input lexicon but only one of the two in the romanization
file will not convert it properly.

WARNING: Beware of romanizations bleeding into each other! This program modifies the whole input memory IN-PLACE, with
one char>IPA pair at a time. The IPA of one romanized character may be the romanization of a different IPA value.
Digraphs, trigraphs or longer are recommended to be placed near the top of the file.
