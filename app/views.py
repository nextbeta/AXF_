import hashlib
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtype, Goods, User


def home(request):

    # 获取轮播图数据
    wheels = Wheel.objects.all()

    # 获取导航数据
    navs = Nav.objects.all()

    # 获取每日必购数据
    mustbuys = Mustbuy.objects.all()

    # 商品部分数据
    shops = Shop.objects.all()  # 所有
    shophead = shops[0]
    shoptabs = shops[1:3]
    shopclass = shops[3:7]
    shopcommends = shops[7:11]

    # 商品列表
    mainShows = MainShow.objects.all()

    data = {
        'wheels':wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead': shophead,
        'shoptabs': shoptabs,
        'shopclass': shopclass,
        'shopcommends': shopcommends,
        'mainShows': mainShows
    }

    return render(request, 'home/home.html', context=data)

def marketbase(request):
    # 默认是热销榜， 全部分类， 综合排序
    return redirect('axf:market', 104749, 0, 0)

# 参数1: categoryid 分类
# 参数2: childid 子类
# 参数3: sortid 排序方式
def market(request, categoryid, childid, sortid):
    # 分类信息
    foodtypes = Foodtype.objects.all()

    # 获取 分类下标  >>> typeIndex
    # 没有时，默认为0  >>> 默认热销数据
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    # 根据下标   获取  分类id
    categoryid = foodtypes[typeIndex].typeid

    # 子类信息
    childtypenames = foodtypes[typeIndex].childtypenames
    childtypelist = []
    for item in childtypenames.split('#'):
        # 子类名称: 子类ID
        # print(item)
        temp = item.split(':')
        dir = {
            'childname': temp[0],
            'childid': temp[1]
        }
        childtypelist.append(dir)

    # 商品信息
    # goodslist = Goods.objects.all()[0:10]
    # 商品信息 -- 分类
    # goodslist = Goods.objects.filter(categoryid=categoryid)
    if childid == '0':  # 全部分类
        goodslist = Goods.objects.filter(categoryid=categoryid)
    else:
        goodslist = Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)

    # 0 综合排序
    if sortid == '1':   # 销量排序
        goodslist = goodslist.order_by('-productnum')
    elif sortid == '2': # 价格最低
        goodslist = goodslist.order_by('price')
    elif sortid == '3': # 价格最高
        goodslist = goodslist.order_by('-price')

    data = {
        'foodtypes': foodtypes,
        'goodslist': goodslist,
        'childtypelist': childtypelist,
        'categoryid': categoryid,
        'childid': childid
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    # temp = str(random.randrange(1,36))
    return render(request, 'cart/cart.html')
    # return HttpResponse('座位号: ' + temp)


def mine(request):
    # 获取用户信息
    token = request.session.get('token')

    data = {}

    if token:
        user = User.objects.get(token=token)
        data['name'] = user.name
        data['img'] = user.img
        data['rank'] = user.rank

    return render(request, 'mine/mine.html', context=data)


import time
def generate_token():
    md5 = hashlib.md5()
    temp = str(time.time()) + str(random.random())
    md5.update(temp.encode('utf-8'))
    return  md5.hexdigest()


def generate_password(param):
    md5 = hashlib.md5()
    md5.update(param.encode('utf-8'))
    return md5.hexdigest()


def register(request):
    if request.method == 'GET':
        return render(request, 'mine/register.html')
    elif request.method == 'POST':
        user = User()
        user.email = request.POST.get('email')
        user.password = generate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')

        # 状态保持
        user.token = generate_token()
        user.save()
        request.session['token'] = user.token

        return redirect('axf:mine')


def checkemail(request):

    # 邮箱
    email = request.GET.get('email')

    users = User.objects.filter(email=email)
    if users.exists():
        return JsonResponse({'msg': '账号已被占用!', 'status': 0})
    else:
        return JsonResponse({'msg': '账号是可以使用!', 'status': 1})


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(generate_password(password))

        try:
            # 不存在，会抛出异常
            # 多个时，会抛出异常　【email是唯一约束】
            user = User.objects.get(email=email)
            if user.password == generate_password(password):
                user.token = generate_token()
                user.save()
                request.session['token'] = user.token
                return redirect('axf:mine')
            else:
                return render(request, 'mine/login.html', context={'p_err': '密码错误'})
        except:
            return render(request, 'mine/login.html', context={'u_err': '账号不存在'})


def logout(request):
    request.session.flush()
    return redirect('axf:mine')


def addcart(request):
    print('添加购物车请求')
    # 获取token  >> user
    token = request.session.get('token')

    data = {}

    if token:   # 登录
        # 获取用户
        user = User.objects.get(token=token)

    else:   # 没登录
        # ajax操作中，不能重定向
        # ajax异步请求操作，数据的传输
        # 即ajax请求，如果想页面跳转(服务器重定向不了)，客户端处理
        # return redirect('axf:login')
        data['msg'] = '请登录后操作!'
        data['status'] = -1
        return JsonResponse(data)