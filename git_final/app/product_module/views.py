from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from requests import request

from .models import Product, ProductCategory, ProductBrand, ProductGallery, ProductSpecificationValue, ProductReview, \
    ProductSpecification, ProductType
from django.views.generic import ListView, DetailView, View
from site_module.models import SiteBanner
from utils.convertors import group_list
from .forms import ProductReviewForm
import mptt
from mptt.fields import TreeForeignKey


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_module/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        loaded_product: Product = kwargs.get('object')
        requests = self.request
        favorite_product_id = requests.session.get("product_favorites")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)

        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_detail)

        galleries = ProductGallery.objects.filter(product_id=loaded_product.id).all()
        # galleries.insert(0, loaded_product)
        context['galleries'] = list(galleries)

        context['related_products'] = list(
            Product.objects.filter(category=loaded_product.category).all()[:6] | Product.objects.filter(
                brand_id__exact=loaded_product.brand_id).all()[:6])

        product_specification = ProductSpecification.objects.filter(product_type=loaded_product.product_type)
        product_paired_specification = {}
        for key in product_specification:
            value = ProductSpecificationValue.objects.filter(specification=key).first()
            product_paired_specification.update({key: value})

        # todo: improve product_specification sector performance
        # print(product_specification)
        # product_specification = ProductSpecification.objects.filter(
        #     product_type=loaded_product.product_type).prefetch_related('productspecification_set')
        # context['product_specification'] = product_specification
        # print(product_specification)
        product_review_form = ProductReviewForm()

        context.update({'product_review_form': product_review_form})
        context.update({'product_specification': product_paired_specification})

        context['reviews'] = ProductReview.objects.filter(product_id=loaded_product.id, parent=None).order_by(
            '-create_date').prefetch_related('productreview_set')
        context['reviews_count'] = ProductReview.objects.filter(product_id=loaded_product.id).count()
        return context


def show_product_category_tree(request, **kwargs):
    loaded_product: Product = kwargs.get("loaded_product")
    loaded_category = loaded_product.category
    value = loaded_category.get_family()
    return render(request, 'product_module/components/category_tree_components.html',
                  {"category_family": value})

    #
    # def post(self, request: HttpRequest):
    #     print("in")
    #     review_form = ProductReviewForm(request.POST)
    #
    #     if review_form.is_valid():
    #         review_text = review_form.cleaned_data.get('text')
    #         parent_id = review_form.cleaned_data.get('parent')
    #         product_id = int(request.POST.get('product_id'))
    #         product: Product = Product.objects.get(id=product_id)
    #
    #         user = request.user
    #
    #         new_review = ProductReview(product=product, user=user, parent=parent_id, text=review_text)
    #         new_review.save()
    #         return redirect('/')
    #
    #
    #     else:
    #         review_form.add_error('text', 'متن نظر شما نمی تواند خالی باشد')
    #         return redirect(reverse('login_page'))


# todo next update
# class AddProductFavorite(View):
#     def post(self, request):
#         product_id = request.POST["product_id"]
#         product = Product.objects.get(pk=product_id)
#         request.session["product_favorites"] = product_id
#         return redirect(product.get_absolute_url())


class AddProductReview(View):
    def post(self, request: HttpRequest):
        print("in")
        review_form = ProductReviewForm(request.POST)

        if review_form.is_valid():
            review_text = review_form.cleaned_data.get('text')
            parent_id = review_form.cleaned_data.get('parent')
            product_id = int(request.POST.get('product_id'))
            product: Product = Product.objects.get(id=product_id)

            user = request.user

            new_review = ProductReview(product=product, user=user, parent=parent_id, text=review_text)
            new_review.save()
            return redirect(request.META['HTTP_REFERER'])



        else:
            review_form.add_error('text', 'متن نظر شما نمی تواند خالی باشد')


# todo review sql save ajax
#     def post(self, **kwargs):
#         print("in")
#         # review_form = ProductReviewForm(request.POST)
#
#         # if review_form.is_valid():
#         #     review_text = review_form.cleaned_data.get('text')
#         #     parent_id = review_form.cleaned_data.get('parent')
#         product = kwargs['product_id']
#         print(product)
# user = request.user

# new_review = ProductReview(product=product, user=user, parent=parent_id, text=review_text)
# new_review.save()

# else:
#     review_form.add_error('text', 'متن نظر شما نمی تواند خالی باشد')
#     return redirect(reverse('login_page'))

# def add_product_reviews2(request: HttpRequest):
#     print('in')
#     if request.user.is_authenticated:
#         product_id = request.GET.get('product_id')
#         # product_id = 1
#         print(product_id)
#         product_review = request.GET.get('product_review')
#         # product_review = 'SRGRGDGGRDGG'
#         print(product_review)
#         parent_id = request.GET.get('parent_id')
#         # parent_id = 1
#         print(parent_id)
#
#         print(product_id, product_review, parent_id)
#         new_comment = ProductReview(product_id=product_id, text=product_review, user_id=request.user.id,
#                                     parent_id=parent_id)
#         new_comment.save()
#         context = {
#             'reviews': ProductReview.objects.filter(article_id=product_id, parent=None).order_by(
#                 '-create_date').prefetch_related('productreviews_set'),
#             'reviews_count': ProductReview.objects.filter(product_id=product_id).count()
#         }
#         return HttpResponse('response')
#         # return render(request, 'product_module/includes/product_review_partial.html', context)
#
#     return HttpResponse('response')
# ////////////////////////////////////////////////////////////

# *************************************product list view part**********************************
class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):  # get product list
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context

    def get_queryset(self):  # filter product list form get
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None:
            # query = query.filter(category__url_title__iexact=category_name)
            test = ProductCategory.objects.get(url_title__iexact=category_name)
            test = test.get_descendants(include_self=True)
            query = query.filter(category__in=test)

        return query


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, parent=None)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)
