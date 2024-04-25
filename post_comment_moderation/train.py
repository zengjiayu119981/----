import torch
import os
import torch.nn as nn
from tqdm import tqdm
import time
from comment_moderation.model import textCNN
import comment_moderation.data_process.word2vec as gv
import comment_moderation.textCNN_data as textCNN_data

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

# 定义数据集参数
dataLoader_param = {
    'batch_size': 128,
    'shuffle': True,
}


def main():
    # 初始化模型
    print('init net...')
    net = textCNN(textCNN_param)
    weight_file = './data/result/textCNN.pkl'
    if os.path.exists(weight_file):
        print('load weight')
        net.load_state_dict(torch.load(weight_file, map_location=torch.device('cpu')))
    else:
        net.init_weight()
    print(net)
    # 将模型移动到 CPU 上
    net.cpu()

    # 初始化数据集
    print('init dataset...')
    data_loader = textCNN_data.textCNN_dataLoader(dataLoader_param)
    # 定义优化器和损失函数
    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    criterion = nn.NLLLoss()
    # 定义日志记录文件
    log = open('log_{}.txt'.format(time.strftime('%y%m%d%H')), 'w')
    log.write('epoch step loss\n')
    # 开始训练
    print("training...")
    for epoch in tqdm(range(100)):
        sum_loss = []
        for i, (clas, sentences) in enumerate(data_loader):
            optimizer.zero_grad()
            sentences = sentences.type(torch.LongTensor)  # 不再移动到cuda
            clas = clas.type(torch.LongTensor)  # 不再移动到cuda
            out = net(sentences)
            loss = criterion(out, clas)
            sum_loss.append(loss.item())
            loss.backward()
            optimizer.step()

            if (i + 1) % 50 == 0:
                print("epoch:", epoch + 1, "step:", i + 1, "loss:", loss.item())
                data = str(epoch + 1) + ' ' + str(i + 1) + ' ' + str(loss.item()) + '\n'
                log.write(data)
        print("epoch:", epoch + 1, "loss:", sum(sum_loss) / len(sum_loss))
    # 保存模型
    print("save model...")
    torch.save(net.state_dict(), weight_file)

if __name__ == "__main__":
    main()
