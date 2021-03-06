from Application1.models import WhiteListedToken
from Application1.serializer import WhiteListedTokenSerializer

class WhiteListedJWTTokenUtil:

    @staticmethod
    def has_permission(user,jwt_value):
        user_id = user.id
        is_allowed_user = False
        try:
            if WhiteListedToken.objects.get(user=user_id, token=WhiteListedJWTTokenUtil.decoded_token(jwt_value)):
                is_allowed_user = True
        except WhiteListedToken.DoesNotExist:
            is_allowed_user = False
        return is_allowed_user

    @staticmethod
    def decoded_token(jwt_value):
        if type(jwt_value)!=str:
            jwt_value = jwt_value.decode("UTF-8")
        return jwt_value

    @staticmethod
    def delete_token(user,jwt_value):
        white_listed_token_id = WhiteListedToken.objects.get(
                                        user=user.id, 
                                        token=WhiteListedJWTTokenUtil.decoded_token(jwt_value)
                                    )
        if white_listed_token_id:
            white_listed_token_id.delete()

    @staticmethod
    def create_token(user,jwt_value):
        data = {
            "user":user.id,
            "token":WhiteListedJWTTokenUtil.decoded_token(jwt_value)
        }
        blacklisted_token_serializer = WhiteListedTokenSerializer(data=data)
        blacklisted_token_serializer.is_valid(raise_exception=True)
        blacklisted_token_serializer.save()
    
    @staticmethod
    def update_token(user,old_jwt_value,new_jwt_value):
        blacklisted_token_id = WhiteListedToken.objects.get(
                                        user=user.id, 
                                        token=WhiteListedJWTTokenUtil.decoded_token(old_jwt_value)
                                    )
        if blacklisted_token_id:
            blacklisted_token_id.token = WhiteListedJWTTokenUtil.decoded_token(new_jwt_value)
            blacklisted_token_id.save()