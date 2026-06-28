from app.data.profile_store import profile


class ProfileService:

    @staticmethod
    def save_profile(data):

        profile.clear()
        profile.update(data)

        return profile

    @staticmethod
    def get_profile():

        return profile