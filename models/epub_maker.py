# Standard library
import os
import pwd
import time

# Local modules imports
from lib.operate_web import WebControl

# 3rd library
from ebooklib import epub


class ePubMaker:
  def __init__(self, serial_name, writer, book_subtitle, book_number, epub_file_name, root_url, handless=True):
    self.serial_name = serial_name
    self.writer = writer
    self.book_subtitle = book_subtitle
    self.book_number = book_number
    self.epub_file_name = epub_file_name
    self.root_url = root_url
    self.handless = handless

    self.web = {}
    self.txt_file_list = []

  def open_browser(self):
    driver_path = './driver/geckodriver'
    profile_path = '/home/'+pwd.getpwuid(os.getuid()).pw_name+'/.mozilla/firefox/y190nyqv.default-1573138803936'
    self.web = WebControl(url=self.root_url, profile_path='./profile/', handless=self.handless, browser_type='firefox', driver_path=driver_path)
    self.web.browser_url(self.root_url)

  def start_parser(self):
    time.sleep(2)
    chapterList = self.web.find_element('id', 'chapterList').find_elements_by_tag_name('li')
    chapterToGo = []
    for idx, chapter in enumerate(chapterList):
      title = chapter.text
      href = chapter.find_element_by_tag_name('a').get_attribute('href')
      if self.book_number in title:
        chapterToGo.append((title, href))
    for chapter in chapterToGo:
      title = chapter[0]
      href = chapter[1]
      self.copy_chapter(title, href)

    self.web.close_browser()

  def copy_chapter(self, title, href):
    web = self.web
    chapter_title = title
    print(chapter_title)
    web.browser_url(href)
    web.scroller_slip_to()
    time.sleep(0.5)

    text_file_path = ''
    content_text = ''
    while True:
      content = web.find_element('id', 'TextContent')
      content_text = content.text
      new_content_text = ''
      try:
        if content_text.find('（繼續下一頁）') > -1 :
          end_mark_idx = content_text.find('（繼續下一頁）')
          new_content_text = content_text[:end_mark_idx-1]
        elif content_text.find('鉛筆小說') > -1 :
          end_mark_idx = content_text.find('鉛筆小說')
          new_content_text = content_text[:end_mark_idx-1]
      except Exception as e:
        new_content_text = content_text

      finally:
        text_file_path = self.save_to_text_file(chapter_title, new_content_text)

        # to next page
        next_page = web.find_element('xpath', '/html/body/p/a[5]')
        next_page.click()
        web.scroller_slip_to()
        time.sleep(0.5)

        try:
          new_title = web.find_element('id', 'mlfy_main_text').find_element_by_tag_name('h1').text
        except Exception as e:
          break
        if chapter_title not in new_title:
          break
    
    chapter = {}
    chapter[chapter_title] = text_file_path
    self.txt_file_list.append(chapter)
    return

  def save_to_text_file(self, chapter_title,  content_text):
    book_folder = os.path.join('./', 'books', self.serial_name)
    if not os.path.isdir(book_folder):
      os.makedirs(os.path.join(book_folder, 'text', ))
      os.makedirs(os.path.join(book_folder, 'epub'))
    if not os.path.isdir(os.path.join(book_folder, 'text')):
      os.makedirs(os.path.join(book_folder, 'text', ))
    if not os.path.isdir(os.path.join(book_folder, 'epub')):
      os.makedirs(os.path.join(book_folder, 'epub', ))
      
    text_file_path = os.path.join(book_folder, 'text', chapter_title+'.txt')
    file = open(text_file_path, 'a') 
    # content_text = content_text.replace("面", "麵")
    content_text = content_text.replace("鉛筆小說", "")
    content_text = content_text.replace("(www.x23qb.com)", "")
    content_text = content_text.rstrip()
    file.write(content_text)
    file.close() 
    return text_file_path


  def create_epub(self):
    book = epub.EpubBook()

    # set metadata
    book.set_title(self.serial_name+'-'+self.book_number+' '+self.book_subtitle)
    book.set_language('zh-tw')

    book.add_author(self.writer)

    # create and add chapter 
    chapter_list = []
    toc = []
    for chapter_idx, chapter_file_info in enumerate(self.txt_file_list):
      chapter_title = list(chapter_file_info.keys())[0]
      chapter_path = chapter_file_info[chapter_title]

      chapter_title = chapter_title.replace(self.book_number, '')
      chapter_title = chapter_title.replace(self.book_subtitle, '').lstrip()
      # print(chapter_idx, chapter_title, chapter_path)
      html_file_name = 'chap_'+str(chapter_idx+1)+'.xhtml'
      epubChapter = epub.EpubHtml(title=chapter_title, file_name=html_file_name)
      content = '<h1>'+chapter_title+'</h1><p>'+open(chapter_path, 'rb').read().decode('utf-8').replace('\n', '<br/>')+'</p>'
      # content = '<h1>chapter_title</h1><p>aaaa</p>'
      epubChapter.content = content.encode()
      chapter_list.append(epubChapter)
      book.add_item(epubChapter)
      toc.append(epub.Link(html_file_name, chapter_title, 'chap-'+str(chapter_idx+1)))

    # define Table Of Contents
    book.toc = tuple(toc)

    # # add cover image
    # book.set_cover("image.jpg", open('12.jpg', 'rb').read())

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # basic spine
    # 把書訂起來
    book.spine = ['nav']+chapter_list

    # write to the file
    epub_folder = os.path.join('./', 'books', self.serial_name, 'epub')
    if not os.path.isdir(epub_folder):
      os.makedirs(epub_folder)
    
    epub_file_path = os.path.join(epub_folder, self.epub_file_name+'.epub')
    epub.write_epub(epub_file_path, book, {})


