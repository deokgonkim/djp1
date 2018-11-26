# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'directory/about.html', {})

def news_factory(request):
    return HttpResponse(newsfactory(), content_type='application/rss+xml')



from django.views.generic import TemplateView
from django.http import HttpResponse

import logging

class User(TemplateView):
    def get(self, req, *args, **kwargs):

        json = {
            #'query': req.query_params,
            'req': req,
            'args': args,
            'kwargs': kwargs
        }
        logging.error(json)
        #return Response(json , status=status.HTTP_200_OK)
        return HttpResponse(json)

# from https://github.com/genonfire/podcast
# -*- coding: utf-8 -*-
from xml.dom import minidom

from django.utils import formats, timezone


def newsfactory():
    u"""뉴스공장"""
    doc = minidom.Document()

    rss = doc.createElement('rss')
    rss.setAttribute(
        'xmlns:itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
    rss.setAttribute('version', '2.0')
    doc.appendChild(rss)

    channel = doc.createElement('channel')
    rss.appendChild(channel)

    title = doc.createElement('title')
    title_text = doc.createTextNode(u'김어준의 뉴스공장')
    title.appendChild(title_text)
    channel.appendChild(title)

    link = doc.createElement('link')
    link_text = doc.createTextNode('https://www.tbs.seoul.kr/cont/FM/NewsFactory/replay/replay.do')
    link.appendChild(link_text)
    channel.appendChild(link)

    summary = doc.createElement('itunes:summary')
    summary_text = doc.createTextNode(u'95.1MHz tbs FM 김어준의 뉴스공장')
    summary.appendChild(summary_text)
    channel.appendChild(summary)

    language = doc.createElement('language')
    language_text = doc.createTextNode('ko-kr')
    language.appendChild(language_text)
    channel.appendChild(language)

    author = doc.createElement('itunes:author')
    author_text = doc.createTextNode('tbs')
    author.appendChild(author_text)
    channel.appendChild(author)

    image = doc.createElement('itunes:image')
    image.setAttribute('href', 'https://www.tbs.seoul.kr/common/images/thumb/fm/thumb_FM_NewsFactory.png')
    channel.appendChild(image)

    explicit = doc.createElement('itunes:explicit')
    explicit_text = doc.createTextNode('no')
    explicit.appendChild(explicit_text)
    channel.appendChild(explicit)

    # ITEM
    weekday = timezone.now().weekday()

    for w in reversed(range(0, weekday + 1)):
        for i in reversed(range(1, 3)):
            if w >= 5:
                continue
            fordate = timezone.now() - timezone.timedelta(days=(weekday - w))
            putdate = fordate.replace(hour=0, minute=30, second=0, microsecond=0)

            now = formats.date_format(putdate, "ymd")
            url = 'http://cdn.podbbang.com/data1/tbsadm/nf%s00%d.mp3' % (now, i)

            item = doc.createElement('item')
            channel.appendChild(item)

            item_title = doc.createElement('title')
            part_text = u' %d-%d부' % (i * 2 - 1, i * 2)
            item_title_text = doc.createTextNode(formats.date_format(putdate, "md") + part_text)
            item_title.appendChild(item_title_text)
            item.appendChild(item_title)

            item_author = author.cloneNode(True)
            item.appendChild(item_author)

            item_summary = summary.cloneNode(True)
            item.appendChild(item_summary)

            date = formats.date_format(putdate, "D, d M Y H:i:s O")
            item_date = doc.createElement('pubDate')
            item_date_text = doc.createTextNode(date)
            item_date.appendChild(item_date_text)
            item.appendChild(item_date)

            item_enclosure = doc.createElement('enclosure')
            item_enclosure.setAttribute('url', url)
            item_enclosure.setAttribute('type', 'audio/mpeg')
            item_enclosure.setAttribute('length', '')
            item.appendChild(item_enclosure)

            guid = doc.createElement('guid')
            guid_text = doc.createTextNode(url)
            guid.appendChild(guid_text)
            item.appendChild(guid)

    xml_str = doc.toprettyxml(encoding='UTF-8', indent='  ')
    return xml_str

