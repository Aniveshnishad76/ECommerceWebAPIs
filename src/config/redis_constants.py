""" Redis Constants """
class RedisKey:
    """ Redis Key Constants"""
    USER_DETAILS                = "user_details1#{email}"
    USER_EXPIRE_SESSION_TOKEN   = "user_expire_session_token#{token}"



class RedisExp:
    """ Redis Exp Constants """
    USER_DETAILS                = 60 * 60 * 24  # 1 day
    USER_EXPIRE_SESSION_TOKEN   = 60 * 60 * 24  # 1 day
