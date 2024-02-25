# import manage
# from django.contrib.auth.hashers import make_password
# from mobile.models import MobileUserModel


# MobileUserModel(
#     full_name="Apple Review",
#     email="review@apple.com",
#     description="Apple Review programm",
#     status=MobileUserModel.Status.ACTIVE,
#     password_hash=make_password("qTyT4x5Z4e7W"),
#     birthday=pendulum.now(),
# ).save(force_insert=True)

"""
GmailSender.render_html_template({
    "text": "You have successfully registered in Clap",
    'pairs': ['Your password: 123']
})

GmailSender.render_html_template({
    "text": "You were fired, thanks for your work!",
    'pairs': [
        'All your sessions have been canceled',
        'You will no longer be able to log into your account',
    ]
})

GmailSender.render_html_template({
    "text": "Your password has been successfully reset!",
    'pairs': [
        'All your sessions have been canceled',
        'Your new password: 123',
    ]
})
"""
