# Standard library
import os

# Local modules imports
from models.epub_maker import ePubMaker
from helper.config_helper import ConfigHelper;

# 3rd library
# pass

def main(book_number, epub_file_name, book_info):
  epub_maker = ePubMaker(
      serial_name = book_info['serial_name'],
      writer = book_info['writer'],
      book_subtitle = '',
      book_number = book_number,
      epub_file_name = epub_file_name,
      root_url = book_info['root_url']
    )
  epub_maker.start_parser()
  epub_maker.create_epub()
  

if __name__ == '__main__':
  

  book_list = [
  # '盾之勇者成名錄.yml',
  # '魔彈之王與戰姬.yml',
  # '怕痛.yml',
  # '地圖化.yml',
  # '女兒是世界最強.yml',
  # '從零開始的異世界生活.yml',
  # '轉生成國王的私生子後.yml',
  # '朋友的妹妹只纏著我.yaml',
  # '平凡職業造就世界最強.yaml',

  # '爆肝工程師的異世界狂想曲.yaml',
  # '看來我的身體天下無敵呢.yaml',
  # '自稱賢者弟子的賢者.yaml',
  
  # '灰與幻想的格林姆迦爾.yaml',
  
  # '靠廢柴技能【狀態異常】.yaml',
  # '有點色公主殿下.yaml',
  # '和神獸在一起.yaml',
  # '創始魔法師.yaml',
  # '幸存煉金術師的城市慢活記.yaml',
  # '軍武宅轉開軍隊後宮.yaml'
  # '女兒已經升到了S級.yaml',
  
  # '田中～年齡等於單身資歷的魔法師～.yaml',
  # '世界最強後衛.yaml',
  # '鐵鏟無雙.yaml',
  '等級封頂的最強劍聖女碧翠斯也有弱點.yaml',
  # '因為不是真正的夥伴而被逐出勇者隊伍.yaml',
  # '勇者以想要成為朋友的視線看了過來！.yaml',
  # '孤單一人的異世界攻略.yaml',
  # '可以讀檔的旅店.yaml',
  ]
  for book_name in book_list:

    cwd = os.getcwd()
    config = ConfigHelper(config_name=book_name, config_path=os.path.join(cwd, 'books_yaml')).get_config()
    # print(config)
   
    books = config['book']['books']
    book_info = config['book']['info']
    for book in books:
      print(book[0], book[1])
      main(book[0], book[1], book_info)