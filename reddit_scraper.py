import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

def get_user_content(username, post_limit=20, comment_limit=30):
    user = reddit.redditor(username)
    posts, comments = [], []

    print(f"\n[🔍] Fetching posts for user: u/{username}...")

    for post in user.submissions.new(limit=post_limit):
        post_data = {
            "title": post.title,
            "body": post.selftext,
            "url": post.url
        }
        print("[📝] Post:", post_data)  # Debug print
        posts.append(post_data)

    print(f"\n[🔍] Fetching comments for user: u/{username}...")

    for comment in user.comments.new(limit=comment_limit):
        comment_data = {
            "body": comment.body,
            "url": f"https://reddit.com{comment.permalink}"
        }
        print("[💬] Comment:", comment_data)  # Debug print
        comments.append(comment_data)

    print(f"\n[📷] Avatar URL: {user.icon_img}")

    return posts, comments, user.icon_img


