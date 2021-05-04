from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Tag, Post
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'create_time', 'owner', 'post_count')  # 页面上要展示的字段
    fields = ('name', 'status', 'is_nav')   # 新增需要填写的字段

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    # 展示该分类下有多少篇文章
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'create_time', 'owner', 'operator')
    list_display_links = []     # 来配置哪些字段可以作为链接，点击它们，可以进入编辑页面

    list_filter = ['category',]     # 页面过滤器
    search_fields = ['title', 'category__name']     # 搜索框搜索字段

    actions_on_top = True   # 动作相关的配置，是否展示在顶部
    actions_on_bottom = True    # 动作相关的配置，是否展示在底部

    # 编辑页面
    save_on_top = True  # 保存、编辑、编辑并新建按钮是否在顶部展示

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    # 自定义参数并展示
    # 参数是固定的，就是当前行的对象。 列表页中的每一行数据都对应数据表中的 一条数据，也对应 Model 的一个实例
    # 同上post_count
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'   # 表头展示的字段

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)