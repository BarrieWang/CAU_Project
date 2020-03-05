import numpy as np
from util.util_mysql import Questions
# from util.util_mysql import UtilMysql as UMysql


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

    return 1 - dis[len1][len2]/max(len1, len2)


def find_qid(args, target, mysql):
    """
    对指定字符串进行查找与匹配
    :param args: 包括最大筛选数量、筛选阈值等参数
    :param target: 目标字符串
    :param mysql: 数据库连接器对象
    :return: 查找结果，list of qid
    """

    temp = mysql.select(Questions)
    temp = {t.qid: suitability(target, t.ques_content) for t in temp}
    temp = sorted(temp.items(), key=lambda kv: kv[1], reverse=True)
    # print(temp)

    result = []
    for key, value in temp:
        if value >= args["threshold"]:
            result.append(key)
    if args["max_num"] is None:
        return result
    else:
        return result[:args["max_num"]]
