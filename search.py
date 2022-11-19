import collections
import collections.abc
from typing import Union, Optional


def is_sequence_forme(obj: object) -> bool:
    """
    Check if obj is sequence

    :param obj: Object
    :return: False if obj is not sequence, else True
    """
    if isinstance(obj, str):
        return False
    return isinstance(obj, collections.abc.Sequence)


def calculate_p(sub_str: str) -> list:
    """
    Calculate p list for substring with len maximum suffixes

    :param sub_str: Substring
    :return: P list with len maximum suffixes
    """
    p = [0] * len(sub_str)
    i = 1
    j = 0
    while i < len(sub_str):
        if sub_str[i] == sub_str[j]:
            p[i] = j + 1
            i += 1
            j += 1
        else:
            if j == 0:
                p[i] = 0
                i += 1
            else:
                j = p[j - 1]

    return p


def find_substr(string: str, sub_str: Union[str, list[str]],
                method: str, count: Optional[int], p: list):
    """
    Implementation of KMP algorythm

    :param string: String
    :param sub_str: Substring(s)
    :param method: Method for search, 'first' - from start, 'last' - form end
    :param count: Count of occurrences
    :param p: P list with len maximum suffixes
    :return:
    """
    k = count
    i = 0
    j = 0
    matches = list()
    while i < len(string):
        if string[i] == sub_str[j]:
            i += 1
            j += 1
            if j == len(sub_str):
                if k is not None:
                    if method == 'last':
                        matches.append(len(string) - i)
                    else:
                        matches.append(i - j)
                    j = p[j - 1]
                    k -= 1
                    if k == 0:
                        return tuple(matches)
                else:
                    if method == 'last':
                        matches.append(len(string) - i)
                    else:
                        matches.append(i - j)
                    j = p[j - 1]
        else:
            if j > 0:
                j = p[j - 1]
            else:
                i += 1

    if len(matches) == 0:
        return None

    return tuple(matches)


def search(string: str, sub_str: Union[str, list[str]],
           case_sensitivity: bool = False, method: str = 'first',
           count: Optional[int] = None) -> Optional[
    Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Search substring in string by KMP

    :param string: String
    :param sub_str: Substring(s)
    :param case_sensitivity: Case sensitivity, True - check, else False
    :param method: Method for search, 'first' - from start, 'last' - form end
    :param count: Count of occurrences
    :return: Indexes were we find substring(s) in string
    """
    if not case_sensitivity:
        string = string.lower()
    if method == 'last':
        string = string[::-1]

    if is_sequence_forme(sub_str):
        string_intersections = {}
        for i in sub_str:
            if len(string) < len(i):
                string_intersections[i] = None
                continue

            temp_str = i[::]
            if not case_sensitivity:
                temp_str = temp_str.lower()

            if method == 'last':
                temp_str = temp_str[::-1]

            p = calculate_p(i)
            string_intersections[i] = find_substr(string, temp_str, method,
                                                  count, p)

        for value in string_intersections.values():
            if value is not None:
                return string_intersections
        return None

    if len(string) < len(sub_str):
        return None

    if not case_sensitivity:
        sub_str = sub_str.lower()

    if method == 'last':
        sub_str = sub_str[::-1]

    p = calculate_p(sub_str)
    return find_substr(string, sub_str, method, count, p)
