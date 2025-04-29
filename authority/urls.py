from django.urls import path


app_name='authority'

from authority.views import authority_main
from authority.views import manage_user
from authority.views import manage_banner
from authority.views import manage_blog
from authority.views import manage_businessinfo
from authority.views import manage_logo
from authority.views import manage_faq
from authority.views import manage_brand
from authority.views import manage_contact
from authority.views import manage_coupon
from authority.views import manage_sitesettings
from authority.views import manage_course
from authority.views import manage_achievement



urlpatterns = [
    path('', authority_main.AdminView.as_view(), name='authority_admin')
]

#Manage User
urlpatterns += [
    path('user-list/', manage_user.UserListView.as_view(), name='user_list'),
    path('login/', manage_user.CustomLoginView.as_view(), name='login'),
    path('logout/',  manage_user.CustomLogoutView.as_view(), name='logout'),
    path('add_admin/', manage_user.AddAdminUserView.as_view(), name='add_admin'),
    path('update_admin/<int:pk>/', manage_user.UpdateAdminUserView.as_view(), name='update_admin'),
    path('reset-password/<int:user_id>/', manage_user.PasswordResetView.as_view(), name='reset_password'),
    path('profile_list/', manage_user.ProfileListView.as_view(), name='profile_list'),
    path('delete_admin/<int:pk>/', manage_user.DeleteUserView.as_view(), name='delete_admin')
]

# Manage Banner
urlpatterns += [
    path('banner-list/', manage_banner.BannerListView.as_view(), name='banner_list'),
    path('banner/add/', manage_banner.AddBannerView.as_view(), name='add_banner'),
    path('banner/update/<int:pk>/', manage_banner.UpdateBannerView.as_view(), name='update_banner'),
    path('banner/delete/<int:pk>/', manage_banner.BannerDeleteView.as_view(), name='delete_banner'),
]

# Manage Blogs
urlpatterns += [
    path('blog-list/', manage_blog.BlogListView.as_view(), name='blog_list'),
    path('blog/add/', manage_blog.AddBlogView.as_view(), name='add_blog'),
    path('blog/update/<int:pk>/', manage_blog.UpdateBlogView.as_view(), name='update_blog'),
    path('blog/delete/<int:pk>/', manage_blog.BlogDeleteView.as_view(), name='delete_blog'),
]
# Manage Blog_Categories
urlpatterns += [
    path('blog/categories/', manage_blog.BlogCategoryListView.as_view(), name='blog_category_list'),
    path('blog/category/add/', manage_blog.AddBlogCategoryView.as_view(), name='add_blog_category'),
    path('blog/category/update/<int:pk>/', manage_blog.UpdateBlogCategoryView.as_view(), name='update_blog_category'),
    path('blog/category/delete/<int:pk>/', manage_blog.BlogCategoryDeleteView.as_view(), name='delete_blog_category'),
]

# Manage Business Info
urlpatterns += [
    path('business-info-list/', manage_businessinfo.BusinessInfoListView.as_view(), name='business_list'),
    path('business-info/add/', manage_businessinfo.AddBusinessInfoView.as_view(), name='add_business_info'),
    path('business-info/update/<int:pk>/', manage_businessinfo.UpdateBusinessInfoView.as_view(), name='update_business_info'),
    path('business-info/delete/<int:pk>/', manage_businessinfo.BusinessInfoDeleteView.as_view(), name='delete_business_info'),
]

# Manage Logo
urlpatterns += [
    path('logo_list/', manage_logo.LogosettingsListView.as_view(), name='logo_list'),
    path('update_logo/<int:pk>/', manage_logo.LogosettingsUpdateView.as_view(), name='update_logo'),
    path('add_logo/', manage_logo.LogosettingsCreateView.as_view(), name='add_logo'),
    path('delete_logo/<int:pk>/', manage_logo.LogosettingsDeleteView.as_view(), name='delete_logo'),

]

# Manage FAQ
urlpatterns += [
    path('faq-list/', manage_faq.FAQListView.as_view(), name='faq_list'),
    path('add_faq/', manage_faq.AddFAQView.as_view(), name='add_faq'),
    path('faq-update/<int:pk>/', manage_faq.UpdateFAQView.as_view(), name='faq_update'),
    path('faq_delete/<int:pk>/', manage_faq.FAQDeleteView.as_view(), name='faq_delete'),
]

# Manage Brand
urlpatterns +=[
    path('brand-list/', manage_brand.BrandListView.as_view(), name='brand_list'),
    path('update-brand/<int:pk>/', manage_brand.UpdateBrandView.as_view(), name='update_brand'),
    path('add-brand/', manage_brand.AddBrandView.as_view(), name='add_brand'),
    path('delete_brand/<int:pk>/', manage_brand.BrandDeleteView.as_view(), name='delete_brand'),
]

# Manage Contact Messages
urlpatterns += [
    path('contact-message-list/', manage_contact.ContactMessageListView.as_view(), name='contact_message_list'),
    path('contact-message/detail/<int:pk>/', manage_contact.ContactMessageDetailView.as_view(), name='contact_message_detail'),
    path('contact-message/delete/<int:pk>/', manage_contact.ContactMessageDeleteView.as_view(), name='delete_contact_message'),
]
# Manage Coupon
urlpatterns += [
    path('coupon_list/', manage_coupon.CouponListView.as_view(), name='coupon_list'),
    path('update_coupon/<int:pk>/',  manage_coupon.CouponUpdateView.as_view(), name='update_coupon'),
    path('add_coupon/',  manage_coupon.AddCouponView.as_view(), name='add_coupon'),
    path('delete_coupon/<int:pk>/', manage_coupon.CouponDeleteView.as_view(), name='delete_coupon'),
]
# Manage Site Settings
urlpatterns += [
    path('site-settings/', manage_sitesettings.SiteSettingsListView.as_view(), name='site_settings'),
    path('site-settings/add/', manage_sitesettings.AddSiteSettingView.as_view(), name='add_site_setting'),
    path('site-settings/<int:pk>/update/', manage_sitesettings.UpdateSiteSettingView.as_view(), name='update_site_setting'),
    path('site-settings/<int:pk>/delete/', manage_sitesettings.SiteSettingDeleteView.as_view(), name='delete_site_setting'),
]

# Manage Course Categories
urlpatterns += [
    path('course-categories/', manage_course.CourseCategoryListView.as_view(), name='course_category_list'),
    path('course-categories/add/', manage_course.AddCourseCategoryView.as_view(), name='add_course_category'),
    path('course-categories/<int:pk>/update/', manage_course.UpdateCourseCategoryView.as_view(), name='update_course_category'),
    path('course-categories/<int:pk>/delete/', manage_course.CourseCategoryDeleteView.as_view(), name='delete_course_category'),
]

# Manage Courses
urlpatterns += [
    path('courses/', manage_course.CourseListView.as_view(), name='course_list'),
    path('courses/add/', manage_course.AddCourseView.as_view(), name='add_course'),
    path('courses/<int:pk>/update/', manage_course.UpdateCourseView.as_view(), name='update_course'),
    path('courses/<int:pk>/delete/', manage_course.CourseDeleteView.as_view(), name='delete_course'),
]
# Manage Course Purchases
urlpatterns += [
    path('course-purchases/', manage_course.CoursePurchaseListView.as_view(), name='course_purchase_list'),
    path('course-purchases/<int:pk>/update/', manage_course.UpdateCoursePurchaseView.as_view(), name='update_course_purchase'),
    path('course-purchases/<int:pk>/delete/', manage_course.CoursePurchaseDeleteView.as_view(), name='delete_course_purchase'),
]
# Manage Achievements
urlpatterns += [
    path('achievements/', manage_achievement.AchievementListView.as_view(), name='achievement_list'),
    path('achievements/add/', manage_achievement.AddAchievementView.as_view(), name='add_achievement'),
    path('achievements/<int:pk>/update/', manage_achievement.UpdateAchievementView.as_view(), name='update_achievement'),
    path('achievements/<int:pk>/delete/', manage_achievement.AchievementDeleteView.as_view(), name='delete_achievement'),
]

