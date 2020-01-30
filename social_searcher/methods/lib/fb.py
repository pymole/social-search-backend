import helpers
import fb_requests as fb_r


def word_rate_fb(obj_id):
    feed = fb_r.get_feed(obj_id)

    # у каждой группы достаем посты
    col = [post['message'] for post in feed]
    return word_rate(col)
