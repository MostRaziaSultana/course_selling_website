from django.shortcuts import render
from .models import Banner,Blog,BlogCategory,FAQ,Brand,Achievement
from Course.models import CourseCategory,Course
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
# Create your views here.
def home(request):
    banners = Banner.objects.first()
    blogs = Blog.objects.filter(show_on_homepage="yes").order_by("-created_at")
    brands = Brand.objects.all()
    counters = Achievement.objects.all()
    categories = CourseCategory.objects.all()
    courses = Course.objects.all()

    return render(request, 'Home/home.html', {
        'banners': banners,
        'blogs': blogs,
        'brands': brands,
        'counters': counters,
        'categories': categories,
        'courses': courses,
    })

def blogs(request):
    blogs = Blog.objects.all()
    total_categories = BlogCategory.objects.count()

    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Blog/all_blog.html', {
        'blogs': page_obj,
    })



def blog_details(request, id):
    blog_details = get_object_or_404(Blog, id=id)
    return render(request, 'Blog/blog_details.html', {
        'blog_details': blog_details,
    })

def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})