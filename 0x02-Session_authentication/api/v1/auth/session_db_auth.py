#!/usr/bin/env python3
"""SessionDBAuth"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Inherits from SessionExpAuth"""
    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession and
        returns the Session ID
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            data = {
                "user_id": user_id,
                "session_id": session_id
            }
            user = UserSession(**data)
            user.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting UserSession in the database
        based on session_id
        """
        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if len(user_sessions) <= 0:
            return None
        current_time = datetime.now()
        time_len = timedelta(seconds=self.session_duration)
        exp_time = user_sessions[0].created_at + time_len
        if exp_time < current_time:
            return None
        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID
        from the request cookie
        """
        session_id = self.session_cookie(request)
        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        if len(user_sessions) <= 0:
            return False
        user_sessions[0].remove()
        return True
