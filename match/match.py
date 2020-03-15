import re
import jieba
import numpy as np
from util.util_mysql import Questions
# from util.util_mysql import UtilMysql as UMysql
from match.soundshapecode.ssc_similarity.compute_ssc_similarity import compute_ssc_similaruty
from match.soundshapecode.variant_kmp import VatiantKMP
from match.soundshapecode.ssc import *
# from classify.classify import Classifier


class Matcher:

    def __init__(self, args):

        self.MAX_NUM = args["max_num"]
        self.SIMILARITY_THRESHOLD = args["threshold"]
        self.SSC_ENCODE_WAY = args["encode_way"]  # 'ALL','SOUND','SHAPE'

        get_hanzi_strokes_dict()
        get_hanzi_structure_dict()
        # generate_hanzi_ssc_file()  # 生成汉字-ssc映射文件
        get_hanzi_ssc_dict()
        # print(hanziStrokesDict)
        # print(hanziStructureDict)
        # print(hanziSSCDict)
        self.kmp = VatiantKMP(self.SIMILARITY_THRESHOLD)

    def word_similarity(self, word, str_):
        """
        在str2中匹配词语str1
        :param word: e.g.'紫琅路'
        :param str_: e.g.'国我爱你女生于无娃哇紫狼路爽晕约紫薇路又刘页列而紫粮路掩连哟罗'
        """

        wordc = get_ssc(word, self.SSC_ENCODE_WAY)
        str_c = get_ssc(str_, self.SSC_ENCODE_WAY)
        self.kmp.index_kmp(str_c, wordc, self.SSC_ENCODE_WAY)

        confidence = 0
        for i in self.kmp.startIdxRes:
            conf = [0]
            for j in range(len(wordc)):
                conf.append(compute_ssc_similaruty(wordc[j], str_c[i + j], self.SSC_ENCODE_WAY))
            confidence = max(confidence, sum(conf))
        return confidence / len(wordc) if len(wordc) > 0 else 0

    def sent_similarity(self, words, str_):
        """
        在str2中匹配句子str1
        """

        conf = []
        str1 = ''.join(re.findall('[\u4e00-\u9fa5]', str_))  # 汉字部分
        str2 = ''.join(re.findall('[0-9a-zA-Z]', str_))  # 字母数字符号部分
        for word in words:
            word = ''.join(re.findall('[0-9a-zA-Z\u4e00-\u9fa5]', word))
            if ''.join(re.findall('[0-9a-zA-Z]', word)) == '':
                temp = self.word_similarity(word, str1)
            else:
                list_ = [
                    suitability(word, str2[start: start + len(word)])
                    for start in range(len(str2) - len(word) + 1)
                ]
                list_.append(suitability(word, str2))
                temp = max(list_)
            # print(temp)
            conf.append(temp)
        return sum(conf) / len(conf) if len(conf) > 0 else 0

    def find(self, target, mysql, classifier):
        """
        对指定字符串进行查找与匹配
        :param target: 目标字符串
        :param mysql: 数据库连接器对象
        :param classifier: 分类器对象
        :return: 查找结果，list of qid
        """

        temp = mysql.select(Questions, Questions.label == classifier.get_label(target))
        words = jieba.cut(target)
        result = {t.qid: self.sent_similarity(words, t.ques_title) for t in temp}
        result = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
        # print(result)

        if self.MAX_NUM is None:
            return [id_ for id_, _ in result]
        else:
            return [id_ for id_, _ in result[:self.MAX_NUM]]


def suitability(str1, str2):
    """
    计算两个字符串的编辑距离
    """

    len1 = len(str1)
    len2 = len(str2)
    dis = np.zeros((len1 + 1, len2 + 1))

    for i in range(len1 + 1):
        dis[i][0] = i
    for j in range(len2 + 1):
        dis[0][j] = j
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            delta = 0 if str1[i - 1] == str2[j - 1] else 1
            dis[i][j] = min(dis[i - 1][j - 1] + delta, min(dis[i - 1][j] + 1, dis[i][j - 1] + 1))

    if len1 > 0 or len2 > 0:
        return 1 - dis[len1][len2] / max(len1, len2)
    else:
        return 0
