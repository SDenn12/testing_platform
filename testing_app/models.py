class CFV:
    @staticmethod
    def invalid_email(email):
        if 3 < len(email) or len(email) > 50:
            if '@' in email:
                punc = list('!"#$%&()*+,/:;<=>?[\]^`{|}~')
                for i in email:
                    if i in punc:
                        return "Email included forbidden characters"
                return "Success"
            else:
                return "There is no @ in the email."
        return "The entered email is too short/long"


    @staticmethod
    def invalid_password(password):
        if 8 <= len(password):
            if len(password) < 50:
                punc = list('(){}[]|`¬¦! "£$%^&*"<>:;#~_-+=,@')
                for i in password:
                    if i in punc:
                        return "Password included forbidden characters"
                return "Success"
            else:
                return "The password is too long"
        else:
            return "The entered password is too short"

    @staticmethod
    def invalid_username(username):
        if 8 <= len(username):
            if len(username) < 50:
                punc = list('!"#$%&()*+,-./:;<=>?@[\]^`{|}~')
                for i in username:
                    if i in punc:
                        return "Username included forbidden characters"
                return "Success"
            else:
                return "The entered username is too long"
        else:
            return "The entered username is too short"

    @staticmethod
    def valid_creds(email, username, password):
        valid_email = CFV.invalid_email(email)
        valid_username = CFV.invalid_username(username)
        valid_password = CFV.invalid_password(password)
        messages = [valid_username, valid_email, valid_password]
        print(messages)
        if messages[0] == messages[1] == messages[2] == "Success":
            return "Success"
        return messages