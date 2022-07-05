import numpy as np
import pandas as pd

from gensim.corpora import Dictionary
from gensim.models import TfidfModel


def get_movie_dataset(movie_path):

    # 读取电影数据
    # number, name, year, director, screenwriter, roles, style, countries, language, date, long, imdb, evaluation
    movie_tags = pd.read_csv(movie_path, usecols=[1, 3, 4, 5, 6, 7, 8, 12]).dropna()

    movies = movie_tags.values.tolist()

    movie_dataset = []
    movie_number = pd.read_csv(movie_path, usecols=[0])
    movie_number = movie_number.values.tolist()
    movie_number = [i[0] for i in movie_number]

    # for i in range(1200,1300):
    #     print(i+1,movies[i][0])
    for movie in movies:
        temp = [movie[0]]
        for _tags in movie[1:5]:
            _tags = _tags[1:-1].replace('\'', '').replace(' ', '').split(',')
            for _tag in _tags:
                temp.append(_tag)
        for _tags in movie[5:7]:
            _tags = _tags.replace(' ', '').split('/')
            for _tag in _tags:
                temp.append(_tag)
        temp.append(movie[7])
        movie_dataset.append(temp)
    # print(movie_dataset)
    print(2)
    return movie_dataset, movie_number


def create_movie_profile(movie_dataset, movie_number):
    dataset = []
    for data in movie_dataset:
        dataset.append(data[1:-1])
    dct = Dictionary(dataset)
    # print(dct)
    corpus = [dct.doc2bow(line) for line in dataset]
    # print(corpus)
    model = TfidfModel(corpus)
    # print(model)
    # print(model[corpus[0]])
    _movie_profile = []
    for i in range(len(movie_dataset)):
        data = movie_dataset[i]
        name = data[0]
        # print(data[-1])
        try:
            score = float(data[-1])
        except:
            score = float(5)
        # print(score)
        vector = model[corpus[i]]
        # print(vector)
        movie_tags_weights = dict(map(lambda x: (dct[x[0]], x[1] * score), vector))
        # print(movie_tags_weights)
        movie_tags = [i[0] for i in movie_tags_weights.items()]
        # print(movie_tags)
        _movie_profile.append((movie_number[i], name, movie_tags, movie_tags_weights))
        # print(i+1,name)
        # print(_movie_profile)
    movie_profile = pd.DataFrame(_movie_profile, columns=["number", "name", "profile", "weights"])
    movie_profile.set_index("number", inplace=True)  # 修改此处可实现id与名字的转换
    # print(movie_profile)
    # print(movie_profile["weights"])
    return movie_profile


def create_inverted_table(movie_profile):
    inverted_table = {}
    for mid, weights in movie_profile['weights'].iteritems():
        # print(mid, weights)
        for tag, weight in weights.items():
            _ = inverted_table.get(tag, [])
            _.append((mid, weight))
            inverted_table.setdefault(tag, _)
    # print(inverted_table)
    return inverted_table


def create_user_profile(movies, movie_profile):
    # movies = [[1, 2], [1, 2], [(OB324390,1, 6.0), (OB324390,2, 8.0)]]
    # watch_record = pd.read_csv(watch_path, usecols=range(3),
    #                            dtype={"userId": np.int32, "movieId": np.int32, "rating": np.float32})
    # watch_record = watch_record.groupby('userId').agg(list)
    user_profile = {}
    # print(watch_record)
    surf_weights,fav_weights,score_weights = 0.3, 1, 0.8
    surf_movie = movies[0]
    fav_movie = movies[1]
    score_movie = movies[2]
    score_movie = pd.DataFrame(score_movie)
    score_movie = score_movie.groupby(0).agg(list)
    # print(score_movie)
    for userId, movieIds, rating in score_movie.itertuples():
        # print(movieIds)
        movieIds = np.array(movieIds)
        rating = np.array(rating)
        user_mean = rating.mean()
        # print(user_mean)
        data_set = np.where(rating >= user_mean)
        # print(data_set)
        final_movieIds = movieIds[data_set]
        # print(final_movieIds)
        user_tag_weight = {}
        for movieId in final_movieIds:
            try:
                movie_data_dict = movie_profile.loc[movieId]['weights']
                # print(movie_data_dict)
                for tag, weight in movie_data_dict.items():
                    # print(tag, weight)
                    if tag in user_tag_weight.keys():
                        user_tag_weight[tag] = (user_tag_weight[tag] + weight)*score_weights
                    else:
                        user_tag_weight[tag] = weight*score_weights
            except:
                print("查无此电影！")  # 此行不会运行，运行到就是数据有问题
        for movieId in surf_movie:
            try:
                movie_data_dict = movie_profile.loc[movieId]['weights']
                # print(movie_data_dict)
                for tag, weight in movie_data_dict.items():
                    # print(tag, weight)
                    if tag in user_tag_weight.keys():
                        user_tag_weight[tag] = (user_tag_weight[tag] + weight)*surf_weights
                    else:
                        user_tag_weight[tag] = weight*surf_weights
            except:
                print("查无此电影！")  # 此行不会运行，运行到就是数据有问题
        for movieId in fav_movie:
            try:
                movie_data_dict = movie_profile.loc[movieId]['weights']
                # print(movie_data_dict)
                for tag, weight in movie_data_dict.items():
                    # print(tag, weight)
                    if tag in user_tag_weight.keys():
                        user_tag_weight[tag] = (user_tag_weight[tag] + weight)*fav_weights
                    else:
                        user_tag_weight[tag] = weight*fav_weights
            except:
                print("查无此电影！")  # 此行不会运行，运行到就是数据有问题
        # print(user_tag_weight)
        # user_tags = sorted(user_tag_weight.items(), key=lambda x: x[1], reverse=True)[:50]
        user_tags = sorted(user_tag_weight.items(), key=lambda x: x[1], reverse=True)
        # print(user_tags)
        user_profile[userId] = user_tags
        # print(movieIds)
        return user_profile, movieIds


def user_recommend_top_N(user_profile, movieIds, inverted_table):
    user_movie_profile = {}
    # print(user_profile)
    for userId, tags in user_profile.items():
        # print(userId)
        movie_weight_dict = {}
        for tags_weight in tags:
            tag = tags_weight[0]
            t_weight = tags_weight[1]
            movie_weight_list = inverted_table[tag]
            for movie_weight in movie_weight_list:
                mid = movie_weight[0]
                m_weight = movie_weight[1]
                # print(movie_weight_dict)
                if mid in movie_weight_dict.keys():
                    movie_weight_dict[mid] += (t_weight * m_weight)
                else:
                    movie_weight_dict[mid] = (t_weight * m_weight)
        # print(movie_weight_dict)
        for movie in movieIds:
            movie_weight_dict.pop(movie, None)
        movie_weight_dict = sorted(movie_weight_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        # print(movie_weight_dict)
        final_movieId = []
        for movie in movie_weight_dict:
            final_movieId.append(movie[0])
        user_movie_profile[userId] = final_movieId
    return user_movie_profile


def filmEvaluation(movie_profile, inverted_table):
    training_path = './data/train_data.csv'
    evaluation_path = './data/rating.csv'
    inverted_table = create_inverted_table(movie_profile)
    user_profile, movieIds = create_user_profile(training_path, movie_profile)
    user_recommend = user_recommend_top_N(user_profile, movieIds, inverted_table)
    name = []
    for item in user_recommend[1]:
        name.append(item[0])
    # print(name)
    ceshi = ['222']
    result = set(name) & set(ceshi)
    print(result)


def recommend(movies):
    movie_path = 'D:\Code\Python\MovieRecommend\data\movie_info.csv'

    # 获取数据，处理数据集

    movie_dataset, movie_number = get_movie_dataset(movie_path)
    # 对电影构建画像

    movie_profile = create_movie_profile(movie_dataset, movie_number)
    # 创建倒排表
    inverted_table = create_inverted_table(movie_profile)
    # 构建用户画像
    user_profile, movieIds = create_user_profile(movies, movie_profile)
    # 对用户推荐电影
    user_recommend = user_recommend_top_N(user_profile, movieIds, inverted_table)
    return user_recommend
    # movie = user_recommend[1]
    # print(movie)
    # filmEvaluation(movie_profile, inverted_table)


# if __name__ == '__main__':
#     recommend(movies=[[1, 2], [1, 2], [(1, 6.0), (2, 8.0)]])
