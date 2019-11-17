class HomeItemType(object):
    BANNER = 'banner'
    CONTENT_TYPE = 'content-type'
    FOLLOWED_CHANNELS = 'followed_channels'
    GENRE = 'genre'
    GROUP = 'group'
    LATEST_UPDATES = 'latest_updates'
    MIXED_ITEMS = 'mixed_items'
    PLAYLIST = 'playlist'
    TOP_BRANDS = 'top_brands'
    PLAYLIST_GROUP = 'playlist_group'
    CONTENTUNIT_GROUP = 'contentunit-group'
    AUDIO_BOOKS_GROUP = 'audio-books-group'
    AUDIO_COURSES_GROUP = 'audio-courses-group'
    CINEMA_CULTURE_STORIES_GROUP = 'cinema-culture-stories-group'
    COMEDY_AUDIO_SHOWS_GROUP = 'comedy-audio-shows-group'
    EDUCATION_EXAM_SHOWS_GROUP = 'education-exam-shows-group'
    FOOD_SHOWS_GROUP = 'food-shows-group'
    HEALTH_SHOWS_GROUP = 'health-shows-group'
    HORROR_CRIME_STORIES_GROUP = 'horror-crime-stories-group'
    KIDS_STORIES_GROUP = 'kids-stories-group'
    LITERATURE_AUDIO_SHOWS_GROUP = 'literature-audio-shows-group'
    LOVE_STORIES_GROUP = 'love-stories-group'
    MOTIVATION_AUDIO_SHOWS_GROUP = 'motivation-audio-shows-group'
    NEW_RELEASED_GROUP = 'new-release-group'
    NEW_USER_GROUP = 'new-user-group'
    POLITICS_AND_NEWS_GROUP = 'politics-and-news-group'
    RECOMMENDED_CHANNELS_GROUP = 'recommended-channels-group'
    RELIGION_STORIES_GROUP = 'religion-stories-group'
    RELIGIOUS_SHOWS_GROUP = 'religious-shows-group'
    RESUME_CHANNELS = 'resume_channels'
    RESUME_CUS = 'resume_cus'
    RADIO = 'radio'
    SELF_HELP_SHOWS_GROUP = 'self-help-shows-group'
    TRENDING_GROUP = 'trending-group'

    VALID_TYPES = ((CONTENT_TYPE, 'ContentType'), (FOLLOWED_CHANNELS, 'FollowedChannels'), (GROUP, 'Group'),
                   (GENRE, 'Genre'), (PLAYLIST_GROUP, 'PlaylistGroup'), (LATEST_UPDATES, 'LatestUpdates'),
                   (NEW_RELEASED_GROUP, 'NewReleasedGroup'), (RESUME_CHANNELS, 'ResumeChannels'), (RADIO, 'Radio'))


HOME_ITEM_TYPES = HomeItemType()
