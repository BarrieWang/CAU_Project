from pypinyin import pinyin, lazy_pinyin, Style
import pypinyin
import pkg_resources

from match.soundshapecode.four_corner import FourCornerMethod
fcm = FourCornerMethod()

# SIMILARITY_THRESHOLD = 0.8
# SSC_ENCODE_WAY = 'ALL'  # 'ALL','SOUND','SHAPE'

yunmuDict = {
    'a': '1', 'o': '2', 'e': '3', 'i': '4', 'u': '5', 'v': '6',
    'ai': '7', 'ei': '7', 'ui': '8',
    'ao': '9', 'ou': 'A', 'iou': 'B',  # 有：you->yiou->iou->iu
    'ie': 'C', 've': 'D', 'er': 'E',
    'an': 'F', 'en': 'G', 'in': 'H', 'un': 'I', 'vn': 'J',  # 晕：yun->yvn->vn->ven
    'ang': 'F', 'eng': 'G', 'ing': 'H', 'ong': 'K'
}

shengmuDict = {
    'b': '1', 'p': '2', 'm': '3', 'f': '4',
    'd': '5', 't': '6', 'n': '7', 'l': '7',
    'g': '8', 'k': '9', 'h': 'A',
    'j': 'B', 'q': 'C', 'x': 'D',
    'zh': 'E', 'ch': 'F', 'sh': 'G', 'r': 'H',
    'z': 'E', 'c': 'F', 's': 'G',
    'y': 'I', 'w': 'J', '0': '0'
}

shapeDict = {
    '⿰': '1', '⿱': '2', '⿲': '3', '⿳': '4', '⿴': '5',  # 左右结构、上下、左中右、上中下、全包围
    '⿵': '6', '⿶': '7', '⿷': '8', '⿸': '9', '⿹': 'A',  # 上三包、下三包、左三包、左上包、右上包
    '⿺': 'B', '⿻': 'C', '0': '0'  # 左下包、镶嵌、独体字：0
}

strokesDict = {
    1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A',
    11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K',
    21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U',
    31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z', 0: '0'
}

hanziStrokesDict = {}  # 汉字笔画数
hanziStructureDict = {}  # 汉字形体结构
hanziSSCDict = {}  # 汉字SSC码


def get_sound_code(one_chi_word):

    res = []
    shengmu_str = pinyin(one_chi_word, style=pypinyin.INITIALS, heteronym=False, strict=False)[0][0]
    if shengmu_str not in shengmuDict:
        shengmu_str = '0'
    
    yunmu_str_fullstrict = pinyin(one_chi_word, style=pypinyin.FINALS_TONE3, heteronym=False, strict=True)[0][0]

    yindiao = '0'
    if yunmu_str_fullstrict[-1] in ['1', '2', '3', '4']:
        yindiao = yunmu_str_fullstrict[-1]
        yunmu_str_fullstrict = yunmu_str_fullstrict[:-1]

    if yunmu_str_fullstrict in yunmuDict:
        # 声母，韵母辅音补码，韵母，音调
        res.append(yunmuDict[yunmu_str_fullstrict])
        res.append(shengmuDict[shengmu_str])
        res.append('0')
    elif len(yunmu_str_fullstrict) > 1:
        res.append(yunmuDict[yunmu_str_fullstrict[1:]])
        res.append(shengmuDict[shengmu_str])
        res.append(yunmuDict[yunmu_str_fullstrict[0]])
    else:
        res.append('0')
        res.append(shengmuDict[shengmu_str])
        res.append('0')
        
    res.append(yindiao)
    return res


def get_shape_code(one_chi_word):

    res = []
    structure_shape = hanziStructureDict.get(one_chi_word, '0')  # 形体结构
    res.append(shapeDict[structure_shape])
    
    four_corner_code = fcm.query(one_chi_word)  # 四角号码（5位数字）
    if four_corner_code is None:
        res.extend(['0', '0', '0', '0', '0'])
    else:
        res.extend(four_corner_code[:])
    
    strokes = hanziStrokesDict.get(one_chi_word, '0')  # 笔画数
    if int(strokes) > 35:
        res.append('Z')
    else:
        res.append(strokesDict[int(strokes)])     
    return res
                

def get_hanzi_strokes_dict():

    strokes_filepath = pkg_resources.resource_filename(__name__, "../../.FILE/zh_data/utf8_strokes.txt")
    with open(strokes_filepath, 'r', encoding='UTF-8') as f:  # 文件特征：
        for line in f:
            line = line.split()
            hanziStrokesDict[line[1]] = line[2]


def get_hanzi_structure_dict():

    structure_filepath = pkg_resources.resource_filename(__name__, "../../.FILE/zh_data/unihan_structure.txt")
    with open(structure_filepath, 'r', encoding='UTF-8') as f:  # 文件特征：U+4EFF\t仿\t⿰亻方\n
        for line in f:
            line = line.split()
            if line[2][0] in shapeDict:
                hanziStructureDict[line[1]] = line[2][0]


def generate_hanzi_ssc_file():

    read_file_path = pkg_resources.resource_filename(__name__, "../../.FILE/zh_data/unihan_structure.txt")
    write_file_path = pkg_resources.resource_filename(__name__, "../../.FILE/zh_data/hanzi_ssc_res.txt")
    write_file = open(write_file_path, "w", encoding='UTF-8')
    with open(read_file_path, 'r', encoding='UTF-8') as f:  # 文件特征：U+4EFF\t仿\t⿰亻方\n
        for line in f:
            line = line.split()
            sound_code = get_sound_code(line[1])
            shape_code = get_shape_code(line[1])
            ssc = "".join(sound_code + shape_code)
            if ssc != '00000000000':
                write_file.write(line[0] + "\t" + line[1] + "\t" + ssc + "\n")
    write_file.close()
    # print('结束！')


def get_hanzi_ssc_dict():

    hanzi_ssc_filepath = pkg_resources.resource_filename(__name__, "../../.FILE/zh_data/hanzi_ssc_res.txt")
    with open(hanzi_ssc_filepath, 'r', encoding='UTF-8') as f:  # 文件特征：U+4EFF\t仿\t音形码\n
        for line in f:
            line = line.split()
            hanziSSCDict[line[1]] = line[2]


def get_ssc(hanzi_sentence, encode_way):

    hanzi_sentence_ssc_list = []
    for one_chi_word in hanzi_sentence:
        ssc = hanziSSCDict.get(one_chi_word, None)
        if ssc is None:
            sound_code = get_sound_code(one_chi_word)
            shape_code = get_shape_code(one_chi_word)
            ssc = "".join(sound_code + shape_code)
        if encode_way == "SOUND":
            ssc = ssc[:4]
        elif encode_way == "SHAPE":
            ssc = ssc[4:]
        else:
            pass
        hanzi_sentence_ssc_list.append(ssc)
    return hanzi_sentence_ssc_list


'''
if __name__ == "__main__":
    """
    1. 声母最多2位，韵母最多3位
    2. 我-国、楼-有、也-列可认为只是声母不一样，而韵母分别看成uo和iou和ie，多出来的部分可看成韵母辅音
    3. 留：liu->l iou     有：you->yiou-> y i ou
    """

    chi_word1 = '紫琅路'
    chi_word2 = '国我爱你女生于无娃哇紫狼路爽晕约紫薇路又刘页列而紫粮路掩连哟罗'
    get_hanzi_strokes_dict()
    get_hanzi_structure_dict()
    # generate_hanzi_ssc_file()  # 生成汉字-ssc映射文件
    get_hanzi_ssc_dict()
    SIMILARITY_THRESHOLD = 0.8
    SSC_ENCODE_WAY = 'ALL'

    chi_word1_ssc = get_ssc(chi_word1, SSC_ENCODE_WAY)
    print(chi_word1_ssc)
    
    chi_word2_ssc = get_ssc(chi_word2, SSC_ENCODE_WAY)
    print(chi_word2_ssc)
    
    # 应用串的模式匹配KMP算法，找变异词。效率比BF算法高
    from match.soundshapecode.variant_kmp import VatiantKMP
    kmp = VatiantKMP(SIMILARITY_THRESHOLD)
    kmp.index_kmp(chi_word2_ssc, chi_word1_ssc, SSC_ENCODE_WAY)  # 主串S、模式串T
    print(kmp.startIdxRes)
    
    variabt_word = set()
    for i in kmp.startIdxRes:
        variabt_word.add(chi_word2[i:i+len(chi_word1)])
    print('变异词：', variabt_word)
'''
    
"""
Created on 2019-4-7
@author: Yoga

Style.TONE3音调显示在末尾
Style.TONE2音调显示在韵母
Style.TONE音调为手写格式(默认)
pypinyin.NORMAL不显示音调
pypinyin.INITIALS显示声母
pypinyin.FINALS显示韵母
pinyin风格参考：http://pypinyin.mozillazg.com/zh_CN/master/api.html#style
strict字段参考：http://pypinyin.mozillazg.com/zh_CN/master/usage.html#strict，默认为True
i处理不包含拼音的字符：http://pypinyin.mozillazg.com/zh_CN/master/usage.html#handle-no-pinyin
i汉语拼音中没有四拼音节：http://www.hanyupinyin.cn/yinjie/yj274.html
i每个基本音节由声母、韵母和声调三个部分组成，有的可以没有声母或声调，但一定有韵母：https://baike.baidu.com/item/%E6%B1%89%E8%AF%AD%E6%8B%BC%E9%9F%B3%E9%9F%B3%E8%8A%82/9167981
i百度汉语笔画：https://hanyu.baidu.com/
i爬虫获取中文笔画数：https://www.cnblogs.com/zhongxinWang/p/8404510.html
i utf8(爬虫)获取中文笔画数：https://blog.csdn.net/zz958712568/article/details/35787139
i unihan获取中文笔画数：https://www.cnblogs.com/Comero/p/8997585.html
                    https://github.com/helmz/Corpus

pinyinStr3 = pinyin(chi_word, style=Style.TONE2, heteronym=False)#heteronym:设置多音字模式
print(pinyinStr3)
pinyinStr4 = pinyin(chi_word, style=Style.TONE3, heteronym=False)#heteronym:设置多音字模式
print(pinyinStr4)
pinyinStr5 = pinyin(chi_word, style=pypinyin.INITIALS, heteronym=False, strict=False)#heteronym:设置多音字模式
print(pinyinStr5)
pinyinStr6 = pinyin(chi_word, style=pypinyin.FINALS_TONE2, heteronym=False, strict=False)#heteronym:设置多音字模式
print(pinyinStr6)
pinyinStr2 = lazy_pinyin(chi_word)
print(pinyinStr2)
"""
