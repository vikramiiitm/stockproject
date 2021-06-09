from django.http.response import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import *
import queue
import threading
from threading import Thread
import time
# Create your views here.

def stockPicker(request):
    stock_picker = tickers_nifty50()
    # print(stock_picker)
    return render(request, 'mainapp/stockpicker.html',{'stock_picker':stock_picker})


def stockTracker(request): 
    stockpicker = request.GET.getlist("stockpicker")
    print(stockpicker)
    data = {}
    available_stocks = tickers_nifty50()

    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("error")

    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    start = time.time()


    # for i in stockpicker:
    #     result = get_quote_table(i)
    #     data.update({i : result})

    for i in range(n_threads):
        thread = Thread(target=lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        result = que.get()
        data.update(result)
        
    end = time.time()
    # print(end-start)
    print(data)
    return render(request, 'mainapp/stocktracker.html',{'data':data})