from django.shortcuts import render
from scripts import psn_cli


# Create your views here.

def psgSearch(request):
    return render(request, 'psGuardSearch.html')


def psgUser(request, nick):
    userInfo = psn_cli.getUsersTitles(nick)
    return render(request, 'psGuardUser.html', context=userInfo)


def psgTitle(request, nick, game):
    titleInfo = psn_cli.getTitlesTrophies(nick, game)
    context = {
        "titleInfo": titleInfo,
        "kwargs": request.GET
    }
    return render(request, 'psGuardTitle.html', context=titleInfo)
