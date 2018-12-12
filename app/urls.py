from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.home, name='index'),   # 首页
    url(r'^home/$', views.home, name='home'),   # 首页

    url(r'^marketbase/$', views.marketbase, name='marketbase'),
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),   # 闪购超市

    url(r'^cart/$', views.cart, name='cart'),   # 购物车
    url(r'^mine/$', views.mine, name='mine'),   # 我的

    url(r'^register/$', views.register, name='register'),   # 注册
    url(r'^checkemail/$', views.checkemail, name=
        'checkemail'),  # 账号验证
    url(r'^login/$', views.login, name='login'),    # 登录
    url(r'^logout/$', views.logout, name='logout'), # 退出

    url(r'^addcart/$', views.addcart, name='addcart'),  # 添加购物车
    url(r'^subcart/$', views.subcart, name='subcart'),  # 删除购物车

    url(r'^changecartstatus/$', views.changecartstatus, name='changecartstatus'),   # 选中状态处理
    url(r'^changecartisall/$', views.changecartisall, name='changecartisall'),      # 全选/取消全选

    url(r'^generateorder/$', views.generateorder, name='generateorder'),    # 下单
    url(r'^orderdetail/(\d+)/$', views.orderdetail, name='orderdetail'),  # 订单详情
    url(r'orderlist/(\d+)/$', views.orderlist, name='orderlist'),
]