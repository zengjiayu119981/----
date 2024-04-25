import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')

# 读取文本文件
file_path = '../data/train.txt'  # 请将 'your_file_path.txt' 替换为实际文件路径
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 提取标签和文本内容
data = []
for line in lines:
    match = re.match(r'__label__(\d)\s+(.*)', line)
    if match:
        label = int(match.group(1))
        text = match.group(2)
        data.append({'label': label, 'text': text})

# 创建数据框
df = pd.DataFrame(data)

# 分词和去停用词
stop_words = set(stopwords.words('english'))  # NLTK的停用词表
df['text'] = df['text'].apply(lambda x: [word.lower() for word in word_tokenize(x) if word.isalnum() and word.lower() not in stop_words])

# 生成词表
vocab = set(word for sublist in df['text'] for word in sublist)
vocab_dict = {word: idx+1 for idx, word in enumerate(vocab)}

# 保存词表及对应索引到新文件
vocab_file_path = '../data/result/word_list.txt'  # 请将 'word_list.txt' 替换为实际文件路径
with open(vocab_file_path, 'w', encoding='utf-8') as vocab_file:
    for word, idx in vocab_dict.items():
        vocab_file.write(f"{word}\t{idx}\n")
