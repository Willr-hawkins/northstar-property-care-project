from django.contrib import admin
from django.utils.html import format_html

admin.site.site_header = "Northstar Property Care"
admin.site.site_title = "Northstar admin"
admin.site.index_title = "Site administration"

def image_thumbnail(image, height=60):
    """ Small preview of an ImageField for admin list and detail pages. """
    if not image:
        return "-"
    return format_html(
        '<img src="{}" alt="" style="height:{}px;width:auto;border-radius:2px">',
        image.url,
        height,
    )
