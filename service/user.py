from service.merchant import MerchantService


class UserService:

    def create_user_visit(self, sess, user_id, merchant):
        if MerchantService().merchant_id_exist(merchant['merchant_id']):
            pass

