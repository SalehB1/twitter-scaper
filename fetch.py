class Fetcher():
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
        self.login_url_1 = 'https://api.twitter.com/1.1/onboarding/task.json?flow_name=login'

    def __get_guest_token(self):
        result = self.session.post("https://api.twitter.com/1.1/guest/activate.json", data='')
        print('X-Guest-Token: ' + result.json()['guest_token'])
        return result.json()['guest_token']

    def __login(self):
        payload = json.dumps({
            "input_flow_data": {
                "flow_context": {
                    "debug_overrides": {},
                    "start_location": {
                        "location": "settings"
                    }
                }
            },
            "subtask_versions": {
                "action_list": 2,
                "alert_dialog": 1,
                "app_download_cta": 1,
                "check_logged_in_account": 1,
                "choice_selection": 3,
                "contacts_live_sync_permission_prompt": 0,
                "cta": 7,
                "email_verification": 2,
                "end_flow": 1,
                "enter_date": 1,
                "enter_email": 2,
                "enter_password": 5,
                "enter_phone": 2,
                "enter_recaptcha": 1,
                "enter_text": 5,
                "enter_username": 2,
                "generic_urt": 3,
                "in_app_notification": 1,
                "interest_picker": 3,
                "js_instrumentation": 1,
                "menu_dialog": 1,
                "notifications_permission_prompt": 2,
                "open_account": 2,
                "open_home_timeline": 1,
                "open_link": 1,
                "phone_verification": 4,
                "privacy_options": 1,
                "security_key": 3,
                "select_avatar": 4,
                "select_banner": 2,
                "settings_list": 7,
                "show_code": 1,
                "sign_up": 2,
                "sign_up_review": 4,
                "tweet_selection_urt": 1,
                "update_users": 1,
                "upload_media": 1,
                "user_recommendations_list": 4,
                "user_recommendations_urt": 1,
                "wait_spinner": 3,
                "web_modal": 1
            }
        })

        def get_flow_token():
            result = self.session.post(self.login_url_1, data=payload)
            if result.json()['status'] == 'success':
                self.flow_token = result.json()['flow_token']
            else:
                raise Exception('Failed to get flow token')

        def step2():
            pass

        def step3():
            pass

        def get_challenge():
            result = self.session.get("https://api.twitter.com/1.1/auth/complete.json")
            return result.json()['challenge']