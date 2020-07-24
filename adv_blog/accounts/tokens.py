from django.contrib.auth.tokens import PasswordResetTokenGenerator
from  six import text_type

class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # return (text_type(user.pk)+ text_type(timestamp)+text_type(user.email))

        user_id = text_type(user.pk)
        ts = text_type(timestamp)
        is_active = text_type(user.is_active)
        return f'{user_id}{ts}{is_active}'  
activation_token = ActivationTokenGenerator()

