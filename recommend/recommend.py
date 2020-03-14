import random
from util.util_mysql import UserCounts, Questions, labels
# from util.util_mysql import UtilMysql as UMysql


def recom_qid(args, mysql, user=None):
    """
    根据当前用户状态提供合适的问题
    :param args: 包括需要的问题推荐数等参数
    :param user: 用户信息对象
    :param mysql: 数据库连接器对象
    :return: 推荐结果，list of qid
    """

    recom_num = args["recom_num"]  # 需要的问题推荐数
    weight = [0.1875, 0.3125, 0.1875, 0.25, 0.0625]  # 各部分得分的权重
    ques = mysql.select(Questions)  # 问题集合

    # 最后的总得分
    score = {q.qid: 0 for q in ques}
    s = [{q.qid: 0 for q in ques} for _ in range(5)]

    if user is not None:
        usercount = mysql.select(UserCounts, UserCounts.uid == user.uid)[0]  # 该用户统计情况

        # 用户初始偏好
        labelset = user.labelset.split(",")
        s[0] = {q.qid: 1 if q.label in labelset else 0 for q in ques}
        # print(s[0]])

        # 用户整体浏览情况
        total_count_1 = usercount.total_count.split(',')
        total_count_2 = usercount.total_count_2.split(',')
        temp1 = {}
        temp2 = {}
        for i in range(len(labels)):
            temp1[labels[i]] = int(total_count_1[i])
            temp2[labels[i]] = int(total_count_2[i])
        max_1 = max(temp1.values())
        max_1 = 1 if max_1 == 0 else max_1
        max_2 = max(temp2.values())
        max_2 = 1 if max_2 == 0 else max_2
        temp = {l: temp1[l] / max_1 * 2/3 + temp2[l] / max_2 * 1/3 for l in labels}
        s[1] = {q.qid: temp[q.label] for q in ques}
        # print(s[1])

        # 用户近期浏览情况，同类提高，本问题减少
        recent_count_1 = usercount.recent_count.split(',')
        recent_count_2 = usercount.recent_count_2.split(',')
        temp1 = {}
        temp2 = {}
        for i in range(len(labels)):
            temp1[labels[i]] = int(recent_count_1[i])
            temp2[labels[i]] = int(recent_count_2[i])
        max_1 = max(temp1.values())
        max_1 = 1 if max_1 == 0 else max_1
        max_2 = max(temp2.values())
        max_2 = 1 if max_2 == 0 else max_2
        temp = {l: temp1[l] / max_1 * 2/3 + temp2[l] / max_2 * 1/3 for l in labels}
        s[2] = {q.qid: temp[q.label] for q in ques}

        recent_qid_1 = usercount.recent_qid.split(',')
        recent_qid_2 = usercount.recent_qid_2.split(',')
        max_1 = len(recent_qid_1)
        max_2 = len(recent_qid_2)
        for i in range(max_1):
            if recent_qid_1[i] != "":
                s[2][recent_qid_1[i]] -= (i + 1) / max_1 * 2/3
        for i in range(max_2):
            if recent_qid_2[i] != "":
                s[2][recent_qid_2[i]] -= (i + 1) / max_2 * 1/3
        # print(s[2])

    # 问题本身质量
    collect = {q.qid: q.ques_collect for q in ques}
    max_ = max(1, max(collect.values()))
    s[3] = {q.qid: collect[q.qid] / max_ for q in ques}
    # print(s[3])

    # 随机浮动，避免出现推荐固化
    s[4] = {q.qid: random.random() for q in ques}
    # print(s[4])

    for q in ques:
        for i in range(5):
            score[q.qid] += s[i][q.qid] * weight[i]
    result = sorted(score.items(), key=lambda kv: kv[1], reverse=True)
    # print(result)
    return [id_ for id_, _ in result[:recom_num]]
