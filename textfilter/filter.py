import re
from collections import defaultdict
from util.util_filepath import read_file

__all__ = ['NaiveFilter', 'BSFilter', 'DFAFilter']


class NaiveFilter:
    """
    过滤关键词表中的关键字
    """

    def __init__(self, file_name="keywords"):
        self.keywords = set([])
        if file_name is not None:
            self.parse(file_name)

    def add(self, keyword):
        self.keywords.add(keyword)

    def parse(self, file_name):
        content = read_file("keyword", file_name, "")
        for keyword in content:
            self.add(keyword.strip().encode("utf-8").lower())

    def filter(self, message, repl="*"):
        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        for kw in self.keywords:
            message = message.replace(kw, repl)
        return message


class BSFilter:
    """
    使用反向排序映射来减少替换时间
    """

    def __init__(self, file_name="keywords"):
        self.keywords = []
        self.kwsets = set([])
        self.bsdict = defaultdict(set)
        self.pat_en = re.compile(r'^[0-9a-zA-Z]+$')  # english phrase or not
        if file_name is not None:
            self.parse(file_name)

    def add(self, keyword):
        if keyword not in self.kwsets:
            self.keywords.append(keyword)
            self.kwsets.add(keyword)
            index = len(self.keywords) - 1
            for word in keyword.split():
                if self.pat_en.search(word):
                    self.bsdict[word].add(index)
                else:
                    for char in word:
                        self.bsdict[char].add(index)

    def parse(self, file_name):
        content = read_file("keyword", file_name, "")
        for keyword in content:
            self.add(keyword.strip().encode("utf-8").lower())

    def filter(self, message, repl="*"):
        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        for word in message.split():
            if self.pat_en.search(word):
                for index in self.bsdict[word]:
                    message = message.replace(self.keywords[index], repl)
            else:
                for char in word:
                    for index in self.bsdict[char]:
                        message = message.replace(self.keywords[index], repl)
        return message


class DFAFilter:
    """
    使用DFA保持算法不断执行
    """

    def __init__(self, file_name="keywords"):
        self.keyword_chains = {}
        self.delimit = '\x00'
        if file_name is not None:
            self.parse(file_name)

    def add(self, keyword):
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        last_level = {}
        last_char = ""
        i = 0
        while i < len(chars):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
            i += 1
        if i == len(chars):
            level[self.delimit] = 0

    def parse(self, file_name):
        content = read_file("keyword", file_name, "")
        for keyword in content:
            self.add(keyword.strip().encode("utf-8").lower())

    def filter(self, message, repl="*"):
        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return ''.join(ret)
