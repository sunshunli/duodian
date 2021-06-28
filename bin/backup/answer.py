import requests


def baidu(question, answers):
    # 进行百度
    url = 'https://www.baidu.com/s'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    data = {
        'wd': question
    }
    res = requests.get(url=url, params=data, headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    for i in range(len(answers)):
        answers[i] = (html.count(answers[i]), answers[i], i)
    answers.sort(reverse=True)
    return answers



def main():
    question = '<<海贼王>>中谁是要成为海贼王的男人'
    # '路飞', 0), (3, '汉库克', 2), (0, '路由器', 1), (0, '路夫', 3)]
    answers = ['路飞', '汉库克', '路由器', '路夫']
    resy = baidu(question, answers)
    resy.sort(key=lambda x:x[0], reverse=True)
    print(resy[0][1])


if __name__ == '__main__':
    main()
