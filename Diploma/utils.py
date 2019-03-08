import re



pattern_access_token = re.compile(
    r'(https://oauth\.vk\.com/blank\.html\#)(access_token=)(\w*)(\&)(\w*)(=)(\w*)(&)(\w*)(=)(\d*)')

