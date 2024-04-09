# In chatbot_detector/admin.py

from django.contrib import admin
from .models import Conversation, ChatbotDetectorModel

admin.site.register(Conversation)
admin.site.register(ChatbotDetectorModel)
