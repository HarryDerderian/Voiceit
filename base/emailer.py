from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
import threading


def welcome_email(user, users_email) :
    # Create a new thread and pass the email parameters to the function
    # This stop the website from being hung up on on sending emails.
    thread = threading.Thread(
        target=__welcome_email,
        args=(user, users_email)
    )
    
    # Start the thread
    thread.start()



def __welcome_email(user, users_email) :
        # Set the subject for the welcome email
        email_subject = "Welcome to Voicelt!"
        # Compose the welcome message with user-specific information
        welcome_message = (f"Dear {user},\n\n" +
        "Welcome to Voicelt, your platform for creating change on campus. " +
        "With Voicelt, you can:\n\n" +
        "- Create petitions for campus issues.\n" +
        "- Collect signatures from like-minded students.\n" +
        "- Make a local impact.\n\n" +
        "Join us in bringing positive change to your college. Start now!\n\n" +
        "Sincerely,\n" +
        "The Voicelt Team")
        # Use the django send_mail function to send the welcome email
        send_mail(email_subject, welcome_message, EMAIL_HOST_USER, [users_email], fail_silently = False)



def petition_created_email(user, users_email, petition_title) :
    # Create a new thread and pass the email parameters to the function
    # This stop the website from being hung on up on sending emails.
    thread = threading.Thread(
        target=__petition_created_email__,
        args=(user, users_email, petition_title)
    )
    
    # Start the thread
    thread.start()



def __petition_created_email__(user, users_email, petition_title) :
        # Set the subject for the welcome email
        email_subject = "Your Voicelt Petition Has Been Created"
        # Compose the welcome message with user-specific information
        petition_creation_message = (f"Hey {user},\n\n" +
        f"Congratulations on creating your petition: {petition_title}, on Voicelt! You've taken the first step toward making a positive change on your campus.\n\n" +
        "Now, it's time to gather signatures and build support for your cause. Share your petition with fellow students, friends, and colleagues to help it gain momentum. When you reach your signature goal, we'll notify you with a special message of achievement.\n\n" +
        "Thank you for being an active member of the Voicelt community and for your dedication to making a local impact. Your voice matters, and together, we can create meaningful change on campus.\n\n"
        "Best of luck with your petition, and keep up the great work!\n\n" +
        "Sincerely,\n" + "The Voicelt Team")
        # Use the django send_mail function to send the welcome email
        send_mail(email_subject, petition_creation_message, EMAIL_HOST_USER, [users_email], fail_silently = False)