from django.db import models

# Create your models here.
# In your models.py file

class Conversation(models.Model):
    user_message = models.TextField()  # The user's message
    bot_response = models.TextField()  # The bot's response
    is_human = models.BooleanField()   # Whether the message is from a human or not

    def __str__(self):
        return f'{self.user_message} - {"Human" if self.is_human else "Bot"}'

class ChatbotDetectorModel(models.Model):
    name = models.CharField(max_length=100)  # Name of the model
    description = models.TextField()         # Description of the model
    trained_model_path = models.CharField(max_length=255)  # Path to the trained model file

    def __str__(self):
        return self.name
