import re
pattern = re.compile(r'(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s* |\-*)(\d{3})(\-*)(\d{2})(\-*)(\d{2})')
pattern2 = re.compile(r'^(\w+)(\s|\,*)(\w+)(\s|\,)(\w+)')