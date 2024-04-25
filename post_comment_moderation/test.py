import torch
import os
import numpy as np
import time
from model import textCNN
import data_process.word2vec as gv

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


def get_val_data(file):
    data_set = open(file, 'r').read().split('\n')
    data_set = list(filter(None, data_set))

    return data_set


def parse_net_result(out):
    score = max(out)
    label = np.where(out == score)[0][0]

    return label, score


def main():
    # init net
    print('init net...')
    net = textCNN(textCNN_param)
    weight_file = './data/result/textCNN.pkl'
    if os.path.exists(weight_file):
        print('load weight')
        # net.load_state_dict(torch.load(weight_file))
        net.load_state_dict(torch.load(weight_file, map_location=torch.device('cpu')))
    else:
        print('No weight file!')
        exit()
    print(net)

    # net.cuda()
    net.eval()

    num_all = 0
    num_right = 0
    test_data = get_val_data('./data/result/test_vec.txt')
    # 定义日志记录文件
    log = open('log_test_{}.txt'.format(time.strftime('%y%m%d%H')), 'w')
    for data in test_data:
        num_all += 1
        data = data.split(',')
        label = int(data[0])
        sentence = np.array([int(x) for x in data[1:301]])
        sentence = torch.from_numpy(sentence)
        # predict = net(sentence.unsqueeze(0).type(torch.LongTensor).cuda()).cpu().detach().numpy()[0]
        # 移动数据到CPU
        sentence = sentence.unsqueeze(0).type(torch.LongTensor)
        predict = net(sentence).detach().numpy()[0]
        label_pre, score = parse_net_result(predict)
        if label_pre == label and score > -100:
            num_right += 1
        if num_all % 100 == 0:
            res = 'acc:{}({}/{})'.format(num_right / num_all, num_right, num_all)
            print(res)
            log.write(res + '\n')


if __name__ == "__main__":
    main()
