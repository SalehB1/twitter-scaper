import requests
import json
from typing import List, Dict, Any
from fetch import Fetcher
from tokens import Tokens
from urllib.parse import quote


class Twitter(Fetcher):

    def idToUnparsedTweets(self, tweet_id: str, cursor: str,
                           include_recommended_tweets: bool = False,
                           fetch_fn: callable = Fetcher.default_fetch) -> List[Dict[str, Any]]:
        variables = {
            "focalTweetId": tweet_id,
            "with_rux_injections": include_recommended_tweets,
            "includePromotedContent": False,
            "withCommunity": True,
            "withQuickPromoteEligibilityTweetFields": False,
            "withBirdwatchNotes": False,
            "withSuperFollowsUserFields": False,
            "withDownvotePerspective": False,
            "withReactionsMetadata": False,
            "withReactionsPerspective": False,
            "withSuperFollowsTweetFields": False,
            "withVoice": False,
            "withV2Timeline": True,
            "__fs_responsive_web_like_by_author_enabled": False,
            "__fs_dont_mention_me_view_api_enabled": False,
            "__fs_interactive_text_enabled": True,
            "__fs_responsive_web_uc_gql_enabled": False,
            "__fs_responsive_web_edit_tweet_api_enabled": False
        }
        if cursor != "":
            variables["cursor"] = cursor

        url = Tokens.api_base + "graphql/L1DeQfPt7n3LtTvrBqkJ2g/TweetDetail?variables=" + quote(json.dumps(variables))

        obj = fetch_fn(url, "GET")
        if obj and obj.get("errors"):
            if obj["errors"]["code"] in [215, 200]:
                super()._get_guest_token()
                obj = fetch_fn(url, "GET")
            else:
                print(f"twitter get request error code: {obj['errors']['code']}")

        obj = obj.get("data", {}).get("threaded_conversation_with_injections_v2", {}).get("instructions", [{}])[0]
        tweets = obj.get("entries") or obj.get("moduleItems")
        return tweets

    def get_user_info(self, user_id):
        url = 'https://api.twitter.com/graphql/-xfUfZsnR_zqjFd-IfrN5A/UserByRestId?variables={"userId":"%s","withHighlightedLabel":true}' % user_id
        result = self.session.get(url)
        print(result.json())

    def get_user_tweets(self, user_id):
        url = 'https://api.twitter.com/graphql/-xfUfZsnR_zqjFd-IfrN5A/UserTweets?variables={"userId":"%s","count":20,"withHighlightedLabel":true,"withTweetQuoteCount":true,"includePromotedContent":true,"withTweetResult":false,"withReactions":false}' % user_id
        result = self.session.get(url)
        print(result.json())


if __name__ == '__main__':
    twitter = Twitter()
    r = twitter.session.get("https://twitter.com")
    print(r.json())
    print(r.text)
