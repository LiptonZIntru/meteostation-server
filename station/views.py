import json

import requests
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
import calendar

# Create your views here.
from log.models import Log
from station.models import Station


@csrf_exempt
@require_http_methods(['POST'])
def index(request):
    stations = Station.objects.all()

    for station in stations:
        response = requests.get('http://' + station.ip)
        if response.status_code == 200:
            Log.objects.create(
                station=station,
                temperature=response.json()['temperature'],
                humidity=response.json()['humidity']
            )
    return HttpResponse("Accepted")


def getToday(request, station_id):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    labels = []
    dataset = []

    for i in range(24):
        temperature = 0
        humidity = 0
        logs = Log.objects \
            .filter(station=station_id) \
            .filter(created_at__range=(today_min + datetime.timedelta(hours=i), today_min + datetime.timedelta(hours=i+1))) \
            .order_by('created_at')
        for log in logs:
            temperature += log.temperature
            humidity += log.humidity
        if logs:
            labels.append(
                (today_min + datetime.timedelta(hours=i)).strftime('%H:%M')
            )
            '''dataset.append({
                "x": temperature / len(logs),
                "y": humidity / len(logs),
            })'''
            dataset.append(temperature / len(logs))

    return HttpResponse(json.dumps({
        "labels": labels,
        "dataset": dataset,
    }))


def getYesterday(request, station_id):
    yesterday_min = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=-1), datetime.time.min)
    labels = []
    dataset = []

    for i in range(24):
        temperature = 0
        humidity = 0
        logs = Log.objects \
            .filter(station=station_id) \
            .filter(
            created_at__range=(yesterday_min + datetime.timedelta(hours=i), yesterday_min + datetime.timedelta(hours=i + 1))) \
            .order_by('created_at')
        for log in logs:
            temperature += log.temperature
            humidity += log.humidity
        if logs:
            labels.append(
                (yesterday_min + datetime.timedelta(hours=i)).strftime('%H:%M')
            )
            '''dataset.append({
                "x": temperature / len(logs),
                "y": humidity / len(logs),
            })'''
            dataset.append(temperature / len(logs))

    return HttpResponse(json.dumps({
        "labels": labels,
        "dataset": dataset,
    }))


def getWeek(request, station_id):
    time_types = [
        datetime.timedelta(hours=8),
        datetime.timedelta(hours=20),
    ]
    labels = []
    dataset = []
    today = datetime.datetime.today()
    min_day = datetime.datetime.combine(today - datetime.timedelta(days=today.weekday()), datetime.time.min)

    for i in range(7):
        for a in range(2):
            temperature = 0
            humidity = 0
            if a == 0:
                logs = Log.objects \
                    .filter(station=station_id) \
                    .filter(created_at__range=(min_day + datetime.timedelta(days=i) + time_types[0],
                                               min_day + datetime.timedelta(days=i) + time_types[1]))\
                    .order_by('created_at')
                labels.append(
                    str((min_day + datetime.timedelta(days=i)).strftime('%d.%m.')) + " den"
                )
            else:
                logs = Log.objects \
                    .filter(station=station_id) \
                    .filter(created_at__range=(min_day + datetime.timedelta(days=i),
                                               min_day + datetime.timedelta(days=i+1)))\
                    .exclude(created_at__range=(min_day + datetime.timedelta(days=i) + time_types[0],
                                               min_day + datetime.timedelta(days=i) + time_types[1])) \
                    .order_by('created_at')
                labels.append(
                    str((min_day + datetime.timedelta(days=i)).strftime('%d.%m.')) + " noc"
                )
            for log in logs:
                temperature += log.temperature
                humidity += log.humidity
            if logs:
                '''dataset.append({
                    "x": temperature / len(logs),
                    "y": humidity / len(logs),
                })'''
                dataset.append(temperature / len(logs))
            else:
                '''dataset.append({
                    "x": 0,
                    "y": 0,
                })'''
                dataset.append(0)
    return HttpResponse(json.dumps({
        "labels": labels,
        "dataset": dataset,
    }))


def getMonth(request, station_id):
    labels = []
    dataset = []
    today = datetime.datetime.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    min_month = datetime.datetime.combine(today.replace(day=1), datetime.time.min)

    for i in range(days_in_month):
        temperature = 0
        humidity = 0
        logs = Log.objects \
            .filter(station=station_id) \
            .filter(created_at__range=(min_month + datetime.timedelta(days=i), min_month + datetime.timedelta(days=i+1))).order_by('created_at')
        for log in logs:
            temperature += log.temperature
            humidity += log.humidity
        labels.append(
            (min_month + datetime.timedelta(days=i)).strftime('%d.%m.%Y')
        )
        if logs:
            '''dataset.append({
                "x": temperature / len(logs),
                "y": humidity / len(logs),
            })'''
            dataset.append(temperature / len(logs))
        else:
            '''dataset.append({
                "x": 0,
                "y": 0,
            })'''
            dataset.append(0)
    return HttpResponse(json.dumps({
        "labels": labels,
        "dataset": dataset,
    }))
