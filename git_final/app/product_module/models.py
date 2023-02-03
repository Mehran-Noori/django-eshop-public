from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account_module.models import User
from mptt.models import MPTTModel, TreeForeignKey


class ProductCategory(MPTTModel):
    title = models.CharField(max_length=200, db_index=True, unique=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=200, db_index=True, unique=True, verbose_name=' عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children',
                            verbose_name='دسته بندی مادر')

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        print(self.url_title)
        return reverse('product_list', args={'cat': self.url_title})


class ProductType(models.Model):
    """
    ProductType provide a list of the different types
    of products that are for sale.
    """

    title = models.CharField(verbose_name='نام نوع محصول', max_length=255, unique=True)
    slug = models.CharField(max_length=200, verbose_name='نوع محصول url', unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'نوع محصول'
        verbose_name_plural = 'لیست انواع محصولات'

    def __str__(self):
        return self.title


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name='مشخصات محصول', max_length=255)

    class Meta:
        verbose_name = 'مشخصات محصول'
        verbose_name_plural = 'مشخصات محصول'

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name=' عنوان برند')
    url_title = models.CharField(max_length=200, verbose_name='نام برند در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام نمایش محصول', unique=True)
    url_title = models.CharField(max_length=300, verbose_name='url نام محصول در')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    image = models.ImageField(upload_to='images/product', null=True, blank=True, verbose_name='عکس محصول')
    image_alt = models.CharField(verbose_name="Alturnative text", help_text="Please add alturnative text",
                                 max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(ProductCategory, on_delete=models.RESTRICT, related_name="child")
    brand = models.ForeignKey(ProductBrand, on_delete=models.RESTRICT, null=True, blank=True, verbose_name='برند محصول')
    price = models.IntegerField(verbose_name='قیمت')
    short_description = models.CharField(max_length=5000, db_index=True, null=True, blank=True,
                                         verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    created_at = models.DateTimeField(verbose_name='ساخته شده در', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name='آخرین ویرایش', auto_now=True)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.url_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ("-created_at",)


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(verbose_name=' مقدار اطلاعات محصول', max_length=255, )

    class Meta:
        verbose_name = ' اطلاعات  محصول'
        verbose_name_plural = 'اطلاعات  محصول '

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'

    def __str__(self):
        return self.caption


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')
    alt_text = models.CharField(verbose_name="Alturnative text", help_text=" تصویر را وارد کنید alt لطفا",
                                max_length=255, null=True, blank=True)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='', blank=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصولات'


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربر', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'
