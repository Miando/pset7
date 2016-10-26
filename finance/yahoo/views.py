from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Stock
from django.template import loader
from .forms import QuoteForm, BuyForm
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


def index(request):
    list_of_dict = Stock.objects.values()
    stocks = []
    for dict in list_of_dict:
        dict["total"]= float(dict["shares"])*float(dict["price"])
        stocks.append(dict)
    template = loader.get_template('yahoo/index.html')
    context = {"stocks":stocks}
    return HttpResponse(template.render(context, request))

def quote(request):
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
        result= "A share of " + name +" (" + symbol + ") costs $" + price
        context = {
            "result": result,
        }
        return render(request, 'yahoo/result.html', context)
    else:
        form = QuoteForm()
    return render(request, 'yahoo/quote.html', {'form': form})


def result(request):
    pass

def buy(request):
    form = BuyForm(request.POST)
    if form.is_valid():
        symbol = form.cleaned_data['symbol']
        shares = form.cleaned_data['shares']
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
        if Stock.objects.filter(symbol=symbol):
            stock_sh=Stock.objects.get(symbol=symbol)
            stock = Stock.objects.select_for_update().filter(symbol=symbol)
            stock.update(price=price)
            sh=int(stock_sh.shares)
            new_shares = sh+int(shares)
            stock.update(price=price)
            stock.update(shares=new_shares)
            return render(request, 'yahoo/buy.html', {'form': form})
        stock = form.save(commit=False)
        stock.name = name
        stock.price = price
        stock.symbol = symbol.upper()
        stock.save()
        stocks = Stock.objects.all()
        return render(request, 'yahoo/index.html', {'stocks': stocks})
    else:
        form = BuyForm()
    return render(request, 'yahoo/buy.html', {'form': form})

def sell(request):
    stocks = Stock.objects.all()
    if request.method == 'POST':
        symbol = request.POST.get("sell")
        print (symbol)
        stock = Stock.objects.filter(symbol=symbol)
        stock.delete()
    return render(request, 'yahoo/sell.html', {'stocks': stocks})
