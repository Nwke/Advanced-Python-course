from typing import TypeVar
import re

reg_exp_pattern_access_token = re.compile(
    r'(https://oauth\.vk\.com/blank\.html\#)(access_token=)(\w*)(\&)(\w*)(=)(\w*)(&)(\w*)(=)(\d*)')

StrOrInt = TypeVar('StrOrInt', str, int)
