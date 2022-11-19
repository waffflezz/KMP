import os
import argparse
import termcolor
from search import search


def validate_path(path: str) -> str:
    """
    Validate path

    :param path: Path
    :return: If path is absolute, return normalize path, else build absolute
    path
    """
    if not os.path.isabs(path):
        return os.path.abspath(path)

    return os.path.normpath(path)


def main():
    """
    Entry point of program
    """
    parser = argparse.ArgumentParser(description="Simple script for search "
                                                 "substrings in string")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--string", "-s", dest="string", type=str,
                       help="String were we find substring")
    group.add_argument("--string_path", "-sp", dest="string_path",
                       type=validate_path,
                       help="Path to txt file, were we find substring")

    parser.add_argument("--sub_string", "-ss", dest="sub_str",
                        type=str, nargs="+",
                        help="substring(s)")
    parser.add_argument('--case_sensitivity',
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help="Case sensitivity for string and substrings")
    parser.add_argument("--method", "-m", dest="method", type=str,
                        default="first",
                        help="Method finding substring in string "
                             "(From the end or from the beginning)")
    parser.add_argument("--count", "-c", dest="count", type=int, default=None,
                        help="The number of occurrences of each "
                             "substring in the string")

    args = parser.parse_args()

    if (args.string_path is None and args.string is None) \
            or args.sub_str is None:
        raise parser.error("String and substring must be not empty!")

    elif len(args.sub_str) > 10:
        raise parser.error("Maximum 10 substrings for search!")

    if args.string_path is not None:
        try:
            with open(args.string_path, "r") as file:
                args.string = file.read()
        except FileNotFoundError as e:
            parser.error(f'File {e.filename} not found!')

    indexes = search(args.string, args.sub_str, args.case_sensitivity,
                     args.method, args.count)

    print(f'String: "{args.string}"')
    print(f'Substring(s): {args.sub_str}')

    print('Indexes: ' + str(indexes))

    colors = {
        30: 'grey',
        31: 'red',
        32: 'green',
        33: 'yellow',
        34: 'blue',
        35: 'magenta',
        36: 'cyan',
        37: 'white',
        38: ('grey', 'underline'),
        39: ('red', 'underline'),
    }

    if indexes is None:
        return
    i = 30
    color_string = list(args.string)
    for key, value in indexes.items():
        if value is None:
            continue

        for first_index in value:
            end_index = first_index + len(key)
            if i > 37:
                for j in range(first_index, end_index):
                    color_string[j] = termcolor.colored(args.string[j],
                                                        colors[i][0],
                                                        attrs=[colors[i][1]])
            else:
                for j in range(first_index, end_index):
                    color_string[j] = termcolor.colored(args.string[j], colors[i])

        i += 1

    print(f'Colored string: {"".join(color_string)}')


if __name__ == '__main__':
    main()
