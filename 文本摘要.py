# coding:utf-8
import jieba  # 中文分词模块
import nltk   # 自然语言处理模块

jieba.setLogLevel(jieba.logging.INFO)

texts = '1、光伏产业链强势上涨，光伏50ETF（159864）大涨9.13%。光伏基本面上看，产能释放叠加年末去库，近期光伏板块主产业链价格逐渐趋于见底，底部反转的预期可能一定程度推动板块上涨。后市看，虽然国内光伏增长逐步面临电网消纳瓶颈，同比增速可能放缓，但2024年国内仍有一定的光伏装机需求，行业竞争格局也有望优化。光伏板块持续调整后估值较低，随着产业链库存、价格和盈利基本面逐步触底，可适当关注光伏板块底部反转的机会。2、新能源的另一个方向是储能。整体看，“碳中和”政策下新能源对旧能源的替代是长期趋势，支撑储能长期需求，制约储能行业的不利因素（大储、工商储经济性较弱，户储库存较高）也有一定程度缓解，可继续关注碳中和50ETF（159861）。此外涉及相关零部件制造的机械ETF（516960）估值较低，也可以适当关注，同时把握经济复苏主线及新能源高景气度的投资机会。3、在新能源板块的带动之下，科创板100ETF（588120）上涨2.56%，成交额加倍放量超5亿元。整体来看，在当前市场经济发展结构转型的背景下，科创板100ETF有望成为把握科技领域投资机遇的重要抓手。而且科创板100的行业成分集中度较低，行业覆盖医药、芯片、机械、新能源等，行业分布较为均衡，不易受到单一周期的影响，或更容易受到均衡配置型资金的青睐。'

print(len(texts))
# 将文本分句
def sent_tokenizer(texts):
    start = 0
    i = 0  # 每个字符的位置
    sentences = []
    punt_list = ',.!?:;~，。！？：；～'  # 标点符号

    for text in texts:  # 遍历每一个字符
        if text in punt_list and token not in punt_list:  # 检查标点符号下一个字符是否还是标点
            sentences.append(texts[start:i + 1])  # 当前标点符号位置
            start = i + 1  # start标记到下一句的开头
            i += 1
        else:
            i += 1  # 若不是标点符号，则字符位置继续前移
            token = list(texts[start:i+2]).pop()  # 取下一个字符.pop是删除最后一个
    if start < len(texts):
        sentences.append(texts[start:])  # 这是为了处理文本末尾没有标点符号的情况
    return sentences


sentence = sent_tokenizer(str(texts))
print(sentence)


# 加载停用词
def load_stop_words(file="hit_stopwords.txt"):
    with open(file, "r", encoding="utf-8") as f:
        return f.read().split("\n")

stopwords = load_stop_words()

# 取出高频词后,用nltk统计词频
entence = sent_tokenizer(texts)  # 分句
words = [w for sentence in sentence for w in jieba.cut(sentence) if w not in stopwords if len(w) > 1 and w != '\t']  # 词语，非单词词，同时非符号
wordfre = nltk.FreqDist(words)  # 统计词频
topn_words = [w[0] for w in sorted(wordfre.items(), key=lambda d:d[1], reverse=True)][:20]  # 取出词频最高的20个单词

# 给句子打分
def _score_sentences(sentences, topn_words):
    """参数 sentences：文本组(好句的文本)，
            topn_words：高频词组"""
    scores = []
    sentence_idx = -1  # 初始句子索引标号-1

    # jieba.cut() 将句子分拆成单词
    for s in [list(jieba.cut(s)) for s in sentences]:  # 遍历每一个分句
        sentence_idx += 1  # 句子索引+1。。0表示第一个句子
        word_idx = []  # 存放高频词在分句中的索引位置.得到结果类似：[1, 2, 3, 4, 5]，[0, 1]，[0, 1, 2, 4, 5, 7]
        for w in topn_words:  # 遍历每一个高频词
            try:
                word_idx.append(s.index(w))  # 高频词出现在该分句子中的索引位置
            except ValueError:  # 不在句子中
                pass
        word_idx.sort()
        if len(word_idx) == 0:
            continue

        # 对于两个连续的单词，利用单词位置索引，通过距离阀值计算族
        clusters = []  # 存放的是几个cluster。类似[[0, 1, 2], [4, 5], [7]]
        cluster = [word_idx[0]]  # 存放的是一个类别（簇）类似[0, 1, 2]
        i = 1
        while i < len(word_idx):  # 遍历当前分句中的高频词
            CLUSTER_THRESHOLD = 2  # 举例阈值设为2
            if word_idx[i]-word_idx[i-1] < CLUSTER_THRESHOLD:  # 如果当前高频词索引与前一个高频词索引相差小于2
                cluster.append(word_idx[i])  # 则认为是一类
            else:
                clusters.append(cluster[:])  # 将当前类别添加进clusters=[]
                cluster = [word_idx[i]]  # 新的类别
            i += 1
        clusters.append(cluster)

        # 对每个族打分，每个族类的最大分数是对句子的打分
        max_cluster_score = 0
        for c in clusters:  # 遍历每一个簇
            significant_words_in_cluster = len(c)  # 当前簇的高频词个数
            total_words_in_cluster = c[-1]-c[0] + 1  # 当前簇里最后一个高频词与第一个的距离
            # 每个句子的分数 = 系数1.0 * 高频词个数**2 / 当前簇的高频词个数
            score = 1.0*significant_words_in_cluster*significant_words_in_cluster/total_words_in_cluster
            # 选择1个句子里得分最大的簇的分数作为句子的得分
            if score > max_cluster_score:
                max_cluster_score = score
        # 再把所有句子的得分放到scores的列表中
        scores.append((sentence_idx, max_cluster_score))  # 存放当前分句的最大簇（说明下，一个分解可能有几个簇）存放格式（分句索引，分解最大簇得分）
    return scores


scored_sentences = _score_sentences(sentence, topn_words)
print(scored_sentences)


top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-3:]  # 对得分进行排序，取出3个句子
top_n_scored = sorted(top_n_scored, key=lambda s: s[0])  # 对得分最高的几个分句，进行分句位置排序
c = dict(top_n_summary=[sentence[idx] for (idx, score) in top_n_scored])
print(c)
