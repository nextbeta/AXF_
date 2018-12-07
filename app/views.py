from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtype, Goods


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
    return redirect('axf:market', 104749)

# 参数1: categoryid分类
def market(request, categoryid):
    # 分类信息
    foodtypes = Foodtype.objects.all()

    # 获取 分类下标  >>> typeIndex
    # 没有时，默认为0  >>> 默认热销数据
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    # 根据下标   获取  分类id
    categoryid = foodtypes[typeIndex].typeid

    # 商品信息
    # goodslist = Goods.objects.all()[0:10]
    # 商品信息 -- 分类
    goodslist = Goods.objects.filter(categoryid=categoryid)


    data = {
        'foodtypes': foodtypes,
        'goodslist': goodslist
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    return render(request, 'cart/cart.html')


def mine(request):
    return render(request, 'mine/mine.html')