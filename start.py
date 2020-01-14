# Standard library
import os
import pwd
import time

# Local modules imports
from lib.operate_web import WebControl

# 3rd library
# pass


def main():
	serial_name = 'OVERLORD'
	book_name = 'overlord 13'
	book_number = '第十三卷'
	driver_path = './driver/geckodriver'
	root_url = 'https://www.x23qb.com/book/1230/'
	profile_path = '/home/'+pwd.getpwuid(os.getuid()).pw_name+'/.mozilla/firefox/y190nyqv.default-1573138803936'
	web = WebControl(url=root_url, profile_path='./profile/', handless=False, browser_type='firefox', driver_path=driver_path)
	web.browser_url(root_url)
	time.sleep(2)
	chapterList = web.find_element('id', 'chapterList').find_elements_by_tag_name('li')
	chapterToGo = []
	for idx, chapter in enumerate(chapterList):
		title = chapter.text
		href = chapter.find_element_by_tag_name('a').get_attribute('href')
		if book_number in title:
			chapterToGo.append((title, href))
	for chapter in chapterToGo:
		title = chapter[0]
		href = chapter[1]
		copy_chapter(web, book_name, title, href)

	web.close_browser()


# title = '第十二卷 聖王國的聖騎士 上 第一章 魔皇亞達巴沃'
# href = 'https://www.x23qb.com/book/1230/4342228.html'

def copy_chapter(web, book_name, title, href):
	chapter_title = title
	web.browser_url(href)
	while True:
		content = web.find_element('id', 'TextContent')
		content_text = content.text
		new_content_text = ''
		try:
			end_mark_idx = content_text.index('＞＞')
			new_content_text = content_text[:end_mark_idx-1]
		except Exception as e:
			lines = content.find_elements_by_tag_name('p')
			for line in lines:
				new_content_text += (line.text+'\n')
			pass
		finally:
			# save new_content_text
			save_to_file(book_name, chapter_title, new_content_text)
			# to next page
			next_page = web.find_element('xpath', '/html/body/p/a[5]')
			next_page_url = next_page.get_attribute('href')
			if href[:href.index('.html')] in next_page_url:
				next_page.click()
				# web.browser_url(next_page_url)
				new_title = web.find_element('id', 'mlfy_main_text').find_element_by_tag_name('h1').text
				print('title: ', title)
				print('net title:', new_title)
				while title == new_title:
					time.sleep(2)
					new_title = web.find_element('id', 'mlfy_main_text').find_element_by_tag_name('h1').text
				title = new_title
			else:
				pass
				break
	return

def save_to_file(book_name, title, content_text):
	book_file_path = os.path.join('./','books',book_name+'-'+title+'.txt')
	file = open(book_file_path, 'a') 
	file.write(content_text.replace("面", "麵"))
	file.close() 

if __name__ == '__main__':
	main()