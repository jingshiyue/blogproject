from django.db import models

# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)  #时间自动生成
    post = models.ForeignKey('blog.Post',on_delete=models.CASCADE)  #由于一个评论只能属于一篇文章，一篇文章可以有多个评论，是一对多的关系

    def __str__(self):
        return self.text[:20]