class InviteListService:
    """
    CHECK IMPORT METHOD
    """

    def __init__(self):
        self.valid_user = []
        self.valid_email = []
        self.invalid_user = []

    def separation_data(self, data):
        for user in data:
            if user.get("email") in self.valid_email:
                user.update({"status": "Duplicate in list"})
                self.invalid_user.append(user)
                continue
            if user.get("success"):
                self.valid_user.append(user)
                self.valid_email.append(user.get("email"))
            else:
                self.invalid_user.append(user)

        return self.valid_user, self.invalid_user
