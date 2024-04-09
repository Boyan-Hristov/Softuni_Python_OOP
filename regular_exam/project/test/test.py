from unittest import TestCase, main
from project.social_media import SocialMedia


class TestSocialMedia(TestCase):

    def setUp(self) -> None:
        self.social_media = SocialMedia("Elon Musk", "Twitter", 100, "tech")

    def test_correct_init(self):
        self.assertEqual("Elon Musk", self.social_media._username)
        self.assertEqual("Twitter", self.social_media._platform)
        self.assertEqual(None, self.social_media._validate_and_set_platform("Twitter"))
        self.assertEqual(100, self.social_media._followers)
        self.assertEqual("tech", self.social_media._content_type)
        self.assertEqual([], self.social_media._posts)

    def test_platform_setter_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.social_media.platform = "Facebook"
        self.assertEqual("Platform should be one of "
                         "['Instagram', 'YouTube', 'Twitter']",
                         str(ve.exception))

    def test_followers_setter_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.social_media.followers = -1
        self.assertEqual("Followers cannot be negative.", str(ve.exception))

    def test_create_post_post_added(self):
        result = self.social_media.create_post("post content")
        self.assertEqual("New tech post created "
                         "by Elon Musk on Twitter.", result)
        self.assertEqual([{'content': "post content",
                           'likes': 0,
                           'comments': []}],
                         self.social_media._posts)

    def test_like_post_invalid_post_index_raises_value_error(self):
        self.social_media._posts = [{'content': "post content",
                                     'likes': 0,
                                     'comments': []}]
        result = self.social_media.like_post(1)
        self.assertEqual("Invalid post index.", result)
        self.assertEqual(0, self.social_media._posts[0]['likes'])

    def test_like_post_reached_maximum_likes_like_not_added(self):
        self.social_media._posts = [{'content': "post content",
                                     'likes': 10,
                                     'comments': []}]
        result = self.social_media.like_post(0)
        self.assertEqual("Post has reached the maximum number of likes.", result)
        self.assertEqual(10, self.social_media._posts[0]['likes'])

    def test_like_post_like_added(self):
        self.social_media._posts = [{'content': "post content",
                                     'likes': 4,
                                     'comments': []}]
        result = self.social_media.like_post(0)
        self.assertEqual("Post liked by Elon Musk.", result)
        self.assertEqual(5, self.social_media._posts[0]['likes'])

    def test_comment_on_post_comment_too_short(self):
        self.social_media._posts = [{'content': "post content",
                                     'likes': 4,
                                     'comments': []}]
        result = self.social_media.comment_on_post(0, "comment")
        self.assertEqual("Comment should be more than 10 characters.", result)
        self.assertEqual([], self.social_media._posts[0]['comments'])

    def test_comment_on_post_comment_added(self):
        self.social_media._posts = [{'content': "post content",
                                     'likes': 4,
                                     'comments': []}]
        result = self.social_media.comment_on_post(0, "comment long enough")
        self.assertEqual("Comment added by Elon Musk on the post.", result)
        self.assertEqual([{'user': "Elon Musk", 'comment': "comment long enough"}],
                         self.social_media._posts[0]['comments'])


if __name__ == "__main__":
    main()
