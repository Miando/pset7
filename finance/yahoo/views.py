from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Stock, History, Cash
from django.template import loader
from .forms import QuoteForm, BuyForm, UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils import timezone

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

def history(request):
    if not request.user.is_authenticated():
        return render(request, 'yahoo/login.html')
    else:
        history= History.objects.filter(user=request.user)
        context = {"history":history}
        return render(request, 'yahoo/history.html', context)


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'yahoo/login.html')
    else:
        list_of_dict = Stock.objects.values().filter(user=request.user)
        stocks = []
        for dict in list_of_dict:
            dict["total"]= float(dict["shares"])*float(dict["price"])
            stocks.append(dict)
        template = loader.get_template('yahoo/index.html')
        cash=Cash.objects.get(user=request.user)
        context = {"stocks":stocks, "cash": cash}
        return HttpResponse(template.render(context, request))

def quote(request):
    if not request.user.is_authenticated():
        return render(request, 'yahoo/login.html')
    else:
        form = QuoteForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']

            link1 = "http://download.finance.yahoo.com/d/quotes.csv?s=" + str(symbol) + "&f=sl1d1t1c1ohgv&e=.csv"
            link2 = "http://finance.yahoo.com/d/quotes.csv?s=" + str(symbol) + "&f=nab"
            csv1 = urllib2.urlopen(link1)
            csv2 = urllib2.urlopen(link2)
            for line in csv1:
                price = line.decode('utf8').split(",")[1]
                break
            for row in csv2:
                name= row.decode('utf8').split(",")[0].replace('"', '')
                break
            if price=="N/A":
                context = {
                    'error_message': 'Symbol not found.',
                }
                return render(request, 'yahoo/error.html', context)
            result= "A share of " + name +" (" + symbol.upper()  + ") costs $" + price
            context = {
                "result": result,
            }
            return render(request, 'yahoo/result.html', context)
        else:
            form = QuoteForm()
        return render(request, 'yahoo/quote.html', {'form': form})


def result(request):
    pass

def error(request):
    pass

def buy(request):
    if not request.user.is_authenticated():
        return render(request, 'yahoo/login.html')
    else:
        form = BuyForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol'].upper()
            shares = form.cleaned_data['shares'].upper()
            if shares.isdigit()==False:
                context = {
                'error_message': "Invalid number of shares.",
                }
                return render(request, 'yahoo/error.html', context)
            link1 = "http://download.finance.yahoo.com/d/quotes.csv?s=" + str(symbol) + "&f=sl1d1t1c1ohgv&e=.csv"
            link2 = "http://finance.yahoo.com/d/quotes.csv?s=" + str(symbol) + "&f=nab"
            csv1 = urllib2.urlopen(link1)
            csv2 = urllib2.urlopen(link2)
            for line in csv1:
                price = line.decode('utf8').split(",")[1]
                break
            for row in csv2:
                name = row.decode('utf8').split(",")[0].replace('"', '')
                break
            if Stock.objects.filter(symbol=symbol, user=request.user):
                stock_sh=Stock.objects.get(symbol=symbol, user=request.user)
                n = Cash.objects.get(user=request.user)
                money = n.money
                cash = Cash.objects.select_for_update().filter(user=request.user)
                m = float(money) - float(price) * float(shares)
                if m < 0:
                    context = {
                        'error_message': "You can't afford that.",
                    }
                    return render(request, 'yahoo/error.html', context)
                stock = Stock.objects.select_for_update().filter(symbol=symbol, user=request.user)
                stock.update(price=price)
                sh=int(stock_sh.shares)
                new_shares = sh+int(shares)
                stock.update(price=price)
                stock.update(shares=new_shares)
                history = History(data=timezone.now(), user=request.user, transaction='BUY',
                                  symbol=symbol, shares=shares, price=price)
                history.save()

                cash.update(money=m)
                stocks = Stock.objects.filter(user=request.user)
                return redirect('/')
            else:
                n = Cash.objects.get(user=request.user)
                money = n.money
                cash = Cash.objects.select_for_update().filter(user=request.user)
                m = float(money) - float(price) * float(shares)
                if m < 0:
                    context = {
                        'error_message': "You can't afford that.",
                    }
                    return render(request, 'yahoo/error.html', context)
                stock = form.save(commit=False)
                stock.user = request.user
                stock.name = name
                stock.price = price
                stock.symbol = symbol
                stock.save()
                history = History(data=timezone.now(), user=request.user, transaction='BUY',
                                  symbol=symbol, shares=shares, price=price)
                history.save()
                n=Cash.objects.get(user=request.user)
                money=n.money
                cash = Cash.objects.select_for_update().filter(user=request.user,)
                m=float(money)-float(price)*float(shares)
                if m <0:
                    context = {
                        'error_message': "You can't afford that.",
                    }
                    return render(request, 'yahoo/error.html', context)
                cash.update(money=m)
                stocks = Stock.objects.filter(user=request.user)
                return redirect('/')
        else:
            form = BuyForm()
        return render(request, 'yahoo/buy.html', {'form': form})

def sell(request):
    if not request.user.is_authenticated():
        return render(request, 'yahoo/login.html')
    else:
        stocks = Stock.objects.filter(user=request.user)
        if request.method == 'POST':
            symbol = request.POST.get("sell")
            print (symbol)
            stock = Stock.objects.filter(symbol=symbol, user=request.user)
            a = Stock.objects.get(symbol=symbol, user=request.user)
            shares = a.shares
            link1 = "http://download.finance.yahoo.com/d/quotes.csv?s=" + str(symbol) + "&f=sl1d1t1c1ohgv&e=.csv"
            csv1 = urllib2.urlopen(link1)
            for line in csv1:
                price = line.decode('utf8').split(",")[1]
                break
            history = History(data=timezone.now(), user=request.user, transaction='SELL',
                              symbol=symbol, shares=shares, price=price)
            history.save()
            n = Cash.objects.get(user=request.user)
            money = n.money
            cash = Cash.objects.select_for_update().filter(user=request.user, )
            m = float(money) + float(price) * float(shares)
            cash.update(money=m)
            stock.delete()
        return render(request, 'yahoo/sell.html', {'stocks': stocks})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                stocks = Stock.objects.filter(user=request.user)
                return render(request, 'yahoo/index.html', {'stocks': stocks})
            else:
                return render(request, 'yahoo/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'yahoo/login.html', {'error_message': 'Invalid login'})
    return render(request, 'yahoo/login.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                cash=Cash(money="10000", user=request.user)
                cash.save()
                stocks = Stock.objects.filter(user=request.user)
                cash=Cash.objects.get(user=request.user)
                return render(request, 'yahoo/index.html', {'stocks': stocks, "cash":cash})

    context = {
        "form": form,
    }
    return render(request, 'yahoo/register.html', context)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'yahoo/login.html', context)