"""Format gml script."""

import itertools as it
import string
from pathlib import Path


def line_remove_semicolons(line: str) -> str:
    """Remove redundant semicolons at the end of the line.

    :param line: Line to format.
    :return: Formatted line.
    """
    line_stripped = line.strip()
    if (
        line_stripped
        and line_stripped.endswith(';')
        and not line_stripped.startswith('var')
    ):
        # remove the semicolon
        return line[:-1]
    return line


def line_remove_mid_spaces(line: str) -> str:  # noqa: C901
    """Remove redundant spaces in the middle of the line.

    :param line: Line to format.
    :return: Formatted line.
    """
    # remove spaces in the middle
    chars: list[str] = []
    start = True
    in_str = False
    for idx, char in enumerate(line):
        push = True
        # juncture for breaks
        for _ in [0]:
            # check if we are inside a string
            if char == '"':
                in_str = not in_str
            if in_str:
                break
            # don't exclude non-whitespace chars
            if char != ' ':
                assert char == '\t' or char not in string.whitespace
                start = False
                break
            # don't do checks at the edges of the string
            if idx == 0 or idx == len(line) - 1:
                break
            # don't exclude whitespaces at the start of the line
            if start:
                break

            # check stuff around the space
            char_left = line[idx - 1]
            char_right = line[idx + 1]
            # characters that can't appear on both sides
            chars_bad_both = set(string.ascii_letters + string.digits + '_')
            # characters that can't appear on either side
            chars_bad_any = '{}'
            if char_left in chars_bad_both and char_right in chars_bad_both:
                break
            if char_left in chars_bad_any or char_right in chars_bad_any:
                break

            push = False
        if push:
            chars.append(char)
    assert not in_str
    return ''.join(chars)


def line_replace_keyword(line: str) -> str:
    """Replace certain keywords in the line.

    :param line: Line to format.
    :return: Formatted line.
    """
    return line.replace('&&', ' and ').replace('||', ' or ')


def format_line(line: str) -> str:
    """Apply all formatting to given line.

    :param line: Line to format.
    :return: Formatted line.
    """
    # remove semicolons
    line = line_remove_semicolons(line)

    # remove spaces at the end
    line = line.rstrip()

    # remove spaces in the middle
    line = line_remove_mid_spaces(line)

    # replace keywords
    return line_replace_keyword(line)


def main(root_dirname: str) -> None:
    """Main function.

    :param root_dirname: Root directory of project.
    """
    root_path = Path(root_dirname)
    scripts_path = root_path / 'scripts'
    if not scripts_path.exists():
        raise FileNotFoundError("Couldn't find scripts folder in project")
    objects_path = root_path / 'objects'
    if not objects_path.exists():
        raise FileNotFoundError("Couldn't find objects folder in project")

    for script_fname in it.chain(
        scripts_path.iterdir(), objects_path.iterdir()
    ):
        if script_fname.suffix != '.gml':
            continue
        print(f'File {script_fname} ...', end=' ')
        content = script_fname.read_text(encoding='utf-8').splitlines()
        skip = 0
        content_formatted: list[str] = []
        for line in content:
            if line.startswith('#'):
                skip = 6
            if line.startswith('/*"/*\'/**//* YYD ACTION'):
                skip = 5
            if line.startswith('//field'):
                skip = 1

            if skip:
                skip -= 1
            else:
                line = format_line(line)
            content_formatted.append(line)

        script_fname.write_text('\n'.join(content_formatted))
        print('written.')


if __name__ == '__main__':
    import sys

    main(sys.argv[1])
