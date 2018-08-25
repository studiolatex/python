import requests
import json
import csv
from datetime import datetime
from time import sleep


def write_json(data):
    with open('posts.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def to_json(post_dict):
    try:
        data = json.load(open('posts_data.json', encoding="utf-8"))
    except:
        data = []

    data.append(post_dict)

    with open('posts_data.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def write_csv(data):
    with open('posts_data.csv', 'a', encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow((data['likes'],
                         data['reposts'],
                         data['comments'],
                         data['text']
                         ))


def get_data(post):
    try:
        post_id = post['id']
    except:
        post_id = 0

    try:
        likes = post['likes']['count']
    except:
        likes = 'zero'

    try:
        reposts = post['reposts']['count']
    except:
        reposts = 'zero'

    try:
        text = post['text']
    except:
        text = '***'

    try:
        comments = post['comments']['count']
    except:
        comments ='zero'

    data = {
        'id': post_id,
        'likes': likes,
        'comments': comments,
        'reposts': reposts,
        'text': text
    }

    return data


def main():
    start = datetime.now()
    # https://api.vk.com/method/wall.get?owner_id=-30666517&count=100&access_token=0a0211150a0211150a021115470a61114600a020a021115510794e9152af88f8e2996ad&v=5.77
    token_service = '0a0211150a0211150a021115470a61114600a020a021115510794e9152af88f8e2996ad'
    group_id = '16603'  # ID группы
    offset = 0
    date_x = 1514764800  # дата в формате timestamp

    all_posts = []

    while True:
        sleep(1)
        r = requests.get('https://api.vk.com/method/wall.get',
                         {'owner_id': group_id, 'count': 100, 'offset': offset, 'v': 5.77,
                          'access_token': token_service})
        posts = r.json()['response']['items']

        all_posts.extend(posts)

        oldest_post_date = posts[-1]['date']

        offset += 100
        print(offset)
        if oldest_post_date < date_x:
            break

    write_json(r.json())  # сперва необходимо получить json файл
    # data_posts = []

    for post in all_posts:
        post_data = get_data(post)
        write_csv(post_data)

    end = datetime.now()

    total = end - start
    print(len(all_posts))
    print(str(total))
    # print(len(all_posts))


if __name__ == "__main__":
    main()
