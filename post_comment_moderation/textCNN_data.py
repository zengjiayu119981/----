from torch.utils.data import Dataset, DataLoader
import random
import numpy as np

train_data = './data/result/train_vec.txt'
valid_data = './data/result/valid_vec.txt'


def get_valid_data(file=valid_data):
    valid_data = open(file, 'r').read().split('\n')
    valid_data = list(filter(None, valid_data))
    random.shuffle(valid_data)

    return valid_data


class textCNN_data(Dataset):
    def __init__(self):
        trainData = open(train_data, 'r').read().split('\n')
        trainData = list(filter(None, trainData))
        random.shuffle(trainData)
        self.trainData = trainData

    def __len__(self):
        return len(self.trainData)

    def __getitem__(self, idx):
        data = self.trainData[idx]
        data = list(filter(None, data.split(',')))
        data = [int(x) for x in data]
        cla = data[0]
        sentence = np.array(data[1:])

        return cla, sentence


def textCNN_dataLoader(param):
    data_set = textCNN_data()
    batch_size = param['batch_size']
    shuffle = param['shuffle']
    return DataLoader(data_set, batch_size=batch_size, shuffle=shuffle)


if __name__ == "__main__":
    dataset = textCNN_data()
    cla, sen = dataset.__getitem__(0)
    # 简单测试
    print(cla)
    print(sen)
