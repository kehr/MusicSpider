#!/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# @File Name:    main.py
# @Author:	     kehr
# @Mail:		 kehr.china@gmail.com
# @Created Time: Sun 13 Apr 2014 02:07:36 PM CST
# @Copyright:    GPL 2.0 applies
# @Description:                     
#########################################################################
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import urllib2
import httplib

class XiamiMusic():

    def __init__(self,url=None):
        httplib.HTTPConnection._http_vsn = 10
        httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
        self.url = url
        self.xiami_url = 'www.xiami.com'
        self.headers = {
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) '
                'Gecko/20091201 Firefox/3.5.6'}
        if self.url is not None:
            self.get_page_content()
    
    def set_page_url(self,url):
        self.url = url
        if self.url is not None:
            self.get_page_content()

    def get_page_content(self):
        '''return page content'''

        req = urllib2.Request(url = self.url, headers = self.headers)
        page = urllib2.urlopen(req)
        #only_main_content = SoupStrainer('div',attrs={'id':'main_content'},)
        #return BeautifulSoup(content,parse_only=only_main_content)
       
        # check url is right
        if page.geturl() == self.url:
            self.content = BeautifulSoup(page.read())
        else:
            self.content = None
      
        return self.content

    def get_singer_info(self):
        """ return the singer's name """
        
        if self.content is None:
            return [],[]

        profile = self.content('div',attrs={'id':'artist_profile'})[0]
        names = profile.div.p.a.contents
        addrs = profile('td')[1].string
        
        if names[1].string is None:
            singer_name = names[0]
        else:
            singer_name = names[0] +' / '+ names[1].string
        
        return singer_name,addrs

    def get_music_basic_info(self):
        """return song's link, name and hot""" 

        if self.content is None:
            return [],[],[]

        music_link = []
        music_name = []
        music_hot  = []

        for music_tag in self.content('td',attrs={'class':'song_name'}):
            music_link.append(self.xiami_url+music_tag.a['href'])
            music_name.append(music_tag.a.string)
        
        for hot_tag in self.content('td',attrs={'class':'song_hot'}):
            music_hot.append(hot_tag.string)

        return music_link,music_name,music_hot

    def get_music_addr(self,link):
        pass

    def put_into_db(self, info):
        pass

if __name__ == '__main__':
    
    music = XiamiMusic()
    
    resut_file = open('result.txt','w+')
    all_count = 1

    for ids in range(85,1000):
        url = 'http://www.xiami.com/artist/top/id/'+str(ids)
        music.set_page_url(url)
        print 'id:',ids,' ',music.get_singer_info()[0],'  ',music.get_singer_info()[1]
        count = 1 

        for pages in range(1,6):
            url += '/page/'+str(pages)
            music.set_page_url(url)
            music_links,music_names,music_hots = music.get_music_basic_info()

            if not music_links:
                print 'Empty ! '
                print '----------------------------------------------------------'
                break
            
            if pages == 1:
                pre_first_link = music_links[0]
            elif pre_first_link != music_links[0]:
                pre_first_link = music_links[0]
            else:
                break
            
            for i,link in enumerate(music_links):
                strformat = '共抓取歌曲%d首 当前曲库编号%d  热度：%s  歌曲地址：%s      歌名：%s'
                strformat = unicode(strformat,'utf-8')
                print strformat % (all_count,count,music_hots[i],link,music_names[i])

                #print '共抓取歌曲',str(all_count),'首 ',str(count),'\t热度: ',music_hots[i],'\t歌曲地址: ',link,'          歌名: ',music_names[i]
                count += 1
                all_count += 1
            else:
                print 'id:',ids,'page:',pages,'end'
                print '----------------------------------------------------------'
        else:
            print 'id:',ids,'end' 
            print '**********************************************************'




