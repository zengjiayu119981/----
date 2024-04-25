import re
import json
from tqdm import tqdm
import jieba
import random

train_data = '../data/train.txt'
valid_data = '../data/dev.txt'
test_data = '../data/test.txt'
stop_word_file = '../data/stop_word.txt'
word_label_file = '../data/result/word_list.txt'
train_data_vec = '../data/result/train_vec.txt'
valid_data_vec = '../data/result/valid_vec.txt'
test_data_vec = '../data/result/test_vec.txt'
# 句子长度
sentence_max_len = 300


def read_stop_word(file):
    data = open(file, 'r', encoding='utf_8').read().split('\n')

    return data


def get_word_dict(file):
    data_set = open(file, 'r', encoding='utf_8').read().split('\n')
    data_set = list(filter(None, data_set))
    word2ind = {}
    for line in data_set:
        # 分割符根据处理文件适配
        line = line.split('\t')
        word2ind[line[0]] = int(line[1])

    ind2word = {word2ind[w]: w for w in word2ind}
    return word2ind, ind2word


def word2vec(vec_file, data_file):
    word2ind, ind2word = get_word_dict(word_label_file)
    vec_txt = open(vec_file, 'w')
    stop_list = read_stop_word(stop_word_file)
    data_set = open(data_file, 'r', encoding='utf_8').read().split('\n')
    data_set = list(filter(None, data_set))
    random.shuffle(data_set)
    special_index = len(word2ind) + 5  # 处理未命中词时的特殊字符（加5是为了区分开常规字符而已，也可以加别的）
    for line in tqdm(data_set):
        match = re.match(r'__label__(\d)\s+(.*)', line)
        label = -1
        text = ''
        if match:
            label = int(match.group(1))
            text = match.group(2)
        else:
            continue
        line_ind = [label]
        text_seg = jieba.cut(text, cut_all=False)
        # 映射成句子向量
        for word in text_seg:
            if word in stop_list:
                continue
            if word in word2ind:
                line_ind.append(word2ind[word])
            else:
                line_ind.append(special_index)
        # 长度截取至定长，-1是减去label部分的长度
        length = line_ind.__len__() - 1
        if length > sentence_max_len:
            line_ind = line_ind[0:sentence_max_len + 2]
        if length < sentence_max_len:
            #  0表示填充字符
            line_ind.extend([0] * (sentence_max_len - length))
        # 写入文件
        for ind in line_ind:
            vec_txt.write(str(ind) + ',')
        vec_txt.write('\n')


if __name__ == '__main__':
    # print('生成训练数据向量：')
    # word2vec(train_data_vec, train_data)
    # print('生成验证数据向量：')
    # word2vec(valid_data_vec, valid_data)
    print('生成测试集向量')
    word2vec(test_data_vec,test_data)
