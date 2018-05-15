from django.shortcuts import render_to_response, get_object_or_404 
from .models import Blog, BlogType 
from django.core.paginator import Paginator
from django.conf import settings

# Create your views here.

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    # 进行分页
    paginator = Paginator(blogs_all_list, settings.BLOGNUM_EACHPAGE)
    # 使用GET请求获取url的页面参数，默认为1
    page_num = request.GET.get('page', 1)
    # 使用django自带的get_page方法，获取页码参数，返回page对象，当参数非法时，自动处理
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前页
    current_page = page_of_blogs.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(current_page - 2, 1), current_page)) + list(range(current_page, min(current_page + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if page_range[-1] - paginator.num_pages <= -2:
        page_range.append('...') 
    # 添加首尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context = {}
    # 获取当前页码中包含的Blog对象列表
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    return render_to_response('blog/blog_list.html', context)

def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)    
    return render_to_response('blog/blog_detail.html', context)

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type = blog_type)
    paginator = Paginator(blogs_all_list, settings.BLOGNUM_EACHPAGE)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    
    context = {}
    context['blog_type'] = blog_type
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    
    return render_to_response('blog/blogs_with_type.html', context)