from django.db import models


# Create your models here.


class ContactUs(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    email = models.EmailField(max_length=300, verbose_name='ایمیل')
    full_name = models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')
    message = models.CharField(max_length=2000, verbose_name='متن')
    create_date = models.TimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    response = models.CharField(max_length=2000, verbose_name='متن پاسخ تماس با ما', null=True, blank=True)
    is_read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')

    class Meta:
        verbose_name = 'تماس با ما '
        verbose_name_plural = ' لیست تماس با ما'

    def __str__(self):
        return self.title
