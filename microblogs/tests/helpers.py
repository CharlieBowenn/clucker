class LogInTester:
    # _auth_user_id only created if there is a user logged in
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
