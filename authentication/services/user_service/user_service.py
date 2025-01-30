from authentication.models import User


class UserService:
    def get_user_by_mobile(self, mobile_number: str):
        try:
            return User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            return None

    def mark_user_verified(self, mobile_number: str):
        user = self.get_user_by_mobile(mobile_number=mobile_number)

        if not user:
            # Return a custom error or raise an exception
            return {"error": "User not found."}

        try:
            # Mark user as verified
            user.is_verified = True
            user.save()  # Save the updated user
            return {"message": "User verified successfully.", "user": user}
        except Exception as e:
            # Handle any error during saving or updating the user
            return {"error": f"Error while verifying user: {str(e)}"}

