import requests
import json
from typing import List, Dict, Any
from fetch import Fetcher


class Twitter(Fetcher):

    def idToUnparsedTweets(tweetID: str, cursor: str,
                           includeRecommendedTweets: bool = False,
                           fetchFn: callable = defaultFetch) -> List[Dict[str, Any]]:
        variables = {
            "focalTweetId": tweetID,
            "with_rux_injections": includeRecommendedTweets,
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

        url = apiBase + "graphql/L1DeQfPt7n3LtTvrBqkJ2g/TweetDetail?variables=" + \
              requests.utils.quote(json.dumps(variables))

        guestToken = currentGuestToken() or await newGuestToken(fetchFn)
        obj = await fetchFn(url, "GET", AUTHORIZATION, guestToken)
        if obj and obj.get("errors"):
            if obj["errors"]["code"] in [215, 200]:
                guestToken = await newGuestToken(fetchFn)
                obj = await fetchFn(url, "GET", AUTHORIZATION, guestToken)
            else:
                print(f"twitter get request error code: {obj['errors']['code']}")

        obj = obj.get("data", {}).get("threaded_conversation_with_injections_v2", {}).get("instructions", [{}])[0]
        tweets = obj.get("entries") or obj.get("moduleItems")
        return tweets


if __name__ == '__main__':
    twitter = Twitter()
    r = twitter.session.get("https://twitter.com")
    print(r.json())
    print(r.text)
