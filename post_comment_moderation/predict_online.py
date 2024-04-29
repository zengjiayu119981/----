import json
import torch
import os
import numpy as np
import time
import jieba
from model import textCNN # 上线就是这么写（Linux）
import data_process.word2vec as gv # 上线就是这么写（Linux）
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = b'_5#y3332323xsspuojcomment'
CORS(app, origins='*')

# 加载词表映射
word2ind, ind2word = gv.get_word_dict('./data/result/word_list.txt')

# 定义模型参数
textCNN_param = {
    'vocab_size': len(word2ind) + 10,
    'embed_dim': 60,
    'class_num': 2,
    "kernel_num": 16,
    "kernel_size": [3, 4, 5],
    "dropout": 0.5,
}

stop_word_file = './data/stop_word.txt'
special_index = len(word2ind) + 5  # 处理未命中词时的特殊字符（加5是为了区分开常规字符而已，也可以加别的）
sentence_max_len = 300

# 启动模型
print('init net...')
net = textCNN(textCNN_param)
weight_file = './data/result/textCNN.pkl'
if os.path.exists(weight_file):
    print('load weight...')
    # net.load_state_dict(torch.load(weight_file))
    net.load_state_dict(torch.load(weight_file, map_location=torch.device('cpu')))
else:
    print('No weight file!')
    exit()
print("模型启动成功：")
print(net)
print()

# 运行模型
net.eval()


def get_val_data(file):
    data_set = open(file, 'r').read().split('\n')
    data_set = list(filter(None, data_set))

    return data_set


def read_stop_word(file):
    data = open(file, 'r', encoding='utf_8').read().split('\n')

    return data


# 加载政治敏感词
illegal1 = read_stop_word('./data/suspect/illegal.txt')
# 加载黑名单词表
illegal2 = read_stop_word('./data/suspect/suspected_illegal.txt')


def parse_comment_list(comments):
    comment_inputs = []
    stop_list = read_stop_word(stop_word_file)
    for comment in comments:
        line_ind = []
        text_seg = jieba.cut(comment, cut_all=False)
        # 映射成句子向量
        for word in text_seg:
            if word in stop_list:
                continue
            if word in word2ind:
                line_ind.append(word2ind[word])
            else:
                line_ind.append(special_index)
        # 长度截取至定长
        length = line_ind.__len__()
        if length > sentence_max_len:
            line_ind = line_ind[0:sentence_max_len + 1]
        if length < sentence_max_len:
            #  0表示填充字符
            line_ind.extend([0] * (sentence_max_len - length))
        comment_inputs.append(line_ind)
    return comment_inputs


def parse_net_result(out):
    # 使用 softmax 对输出进行归一化
    exp_out = np.exp(out - np.max(out))  # 减去最大值，避免数值溢出
    normalized_out = exp_out / np.sum(exp_out)
    # 获取最大概率对应的标签和 score
    label = np.argmax(normalized_out)
    score = normalized_out[label]

    return label, score


# fast-mode
def getCommentModerationResult(comments):
    comment_inputs = parse_comment_list(comments)
    # 将评论输入转换为PyTorch Tensor
    comment_inputs_tensor = torch.LongTensor(comment_inputs)

    # 移动数据到CPU
    comment_inputs_tensor = comment_inputs_tensor.type(torch.LongTensor)

    # 记录开始时间
    start_time = time.time()

    with torch.no_grad():
        predictions = net(comment_inputs_tensor)

    # 记录结束时间
    end_time = time.time()

    # 计算时间差
    elapsed_time = end_time - start_time
    # print(f"运算时间: {elapsed_time} 秒")

    # 解析预测结果
    comment_outputs = {}
    for i in range(len(predictions)):
        prediction = predictions[i]
        label_pre, score = parse_net_result(prediction.numpy())
        comment_outputs[comments[i]] = {'label': int(label_pre), 'score': round(float(score), 6), 'index': int(i)}
    # 组合结果
    res = {
        'results': comment_outputs,
        'costSeconds': round(elapsed_time, 6)
    }
    return res


# accurate-mode
def getAccurateCommentModerationResult(comments, isStrict=False):
    comment_inputs = parse_comment_list(comments)
    # 记录开始时间
    start_time = time.time()
    # 解析预测结果
    comment_outputs = {}
    with torch.no_grad():
        for i in range(len(comment_inputs)):
            comment = comments[i]
            flag = False
            # 黑名单检测
            for w in illegal1:
                if w in comment:
                    comment_outputs[comments[i]] = {'label': 1, 'score': 1.0, 'index': int(i)}
                    flag = True
                    break
            if flag:
                continue
            # 政治敏感词检测
            if isStrict:
                for w in illegal2:
                    if w in comment:
                        comment_outputs[comments[i]] = {'label': 1, 'score': 1.0, 'index': int(i)}
                        flag = True
                        break
                if flag:
                    continue
            comment_input = comment_inputs[i]
            sentence = np.array(comment_input)
            sentence = torch.from_numpy(sentence)
            # 移动数据到CPU
            sentence = sentence.unsqueeze(0).type(torch.LongTensor)
            predict = net(sentence).detach().numpy()[0]
            label_pre, score = parse_net_result(predict)
            comment_outputs[comments[i]] = {'label': int(label_pre), 'score': round(float(score), 6), 'index': int(i)}

    # 记录结束时间
    end_time = time.time()

    # 计算时间差
    elapsed_time = end_time - start_time
    # print(f"运算时间: {elapsed_time} 秒")

    # 组合结果
    res = {
        'results': comment_outputs,
        'costSeconds': round(elapsed_time, 6)
    }
    return res


@app.route('/comment/moderation', methods=['POST'])
def comment_moderation():
    req_time = time.strftime('%Y/%m.%d/%H:%S')
    data = json.loads(request.get_data())
    print('request_time:{}，请求数据：{}'.format(req_time, data))
    comments = data.get('comments')
    print(comments)
    mode = data.get('mode')
    if mode == 'fast':
        res = getCommentModerationResult(comments)
    if mode == 'accurate':
        res = getAccurateCommentModerationResult(comments, False)
    if mode == 'strict':
        res = getAccurateCommentModerationResult(comments, True)
    print('request_time:{}，响应结果：{}'.format(req_time, res))
    return jsonify(res)


if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    app.run(debug=True, host='0.0.0.0', port='9102')
