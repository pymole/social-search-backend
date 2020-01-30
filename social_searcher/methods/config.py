from . import handlers


#
# http://oauth.vk.com/authorize?client_id=7087337&display=page&redirect_uri=http://localhost/&scope=offline&response_type=code&v=5.101
# https://oauth.vk.com/access_token?client_id=7087337&client_secret=SwCdRqguQy76hBEvlS1z&redirect_uri=http://localhost&code=b155f9da739c018beb

METHODS = {
    'vk': {
        'auth_handler': handlers.is_vk_authenticated,
        'methods': {
            'word_rate': handlers.vk_word_rate,
            'user_groups_city': handlers.vk_user_group_city
        }
    }
}
