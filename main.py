import requests
from tokens import Tokens


def main():
    print("Hello World!")
    r = requests.get("https://twitter.com")
    print(r.status_code)
    print(r.text)


class Twitter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Twitter-Active-User': 'yes',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://twitter.com/',
            'Connection': 'keep-alive',
        })
        # self.session.headers.update({'x-csrf-token': Tokens.csrf_token})
        self.session.headers.update({'authorization': Tokens.Authorization})
        self.session.headers.update({'x-guest-token': self.__get_guest_token()})
        self.session.headers.update({
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'})

    def __get_guest_token(self):
        result = self.session.post("https://api.twitter.com/1.1/guest/activate.json", data='')
        print('X-Guest-Token: ' + result.json()['guest_token'])
        return result.json()['guest_token']

    def __login(self):
        def step1():
            pass

        def step2():
            pass

        def step3():
            pass

        def get_challenge():
            result = self.session.get("https://api.twitter.com/1.1/auth/complete.json")
            return result.json()['challenge']


if __name__ == '__main__':
    # main()
    t = Twitter()
    # print(t.session.headers)
    r = t.session.get("https://twitter.com")
    print(r.json())
    print(r.text)
