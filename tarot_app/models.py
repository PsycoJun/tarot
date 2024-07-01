from django.db import models

class ButtonClick(models.Model):
    button_id = models.IntegerField()
    click_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Button {self.button_id} - {self.click_count} clicks"
