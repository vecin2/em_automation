import re


class TaskPrefixGenerator(object):
    def next(self, latest_task_name):
        regex = "^\d+[-_.]"
        prefix_number_list = re.findall(regex, latest_task_name)
        if prefix_number_list:
            latest_prefix = prefix_number_list[0]  # 01_ or 01. or 01-
            latest_str_number = latest_prefix[:-1]  # remove non character string - 01
            next_number = int(latest_str_number) + 1
            # fill zeros and append last character from previous prefix
            result = str(next_number).zfill(len(latest_str_number)) + latest_prefix[-1]
            return result
        return ""
