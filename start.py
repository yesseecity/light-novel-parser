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
    root_url = book_info['root_url'],
    handless=True
  )
  epub_maker.open_browser()
  epub_maker.start_parser()
  epub_maker.create_epub()
  

if __name__ == '__main__':
  

  book_list = [
  # 'full_metal_panic.yaml',
  # '盾之勇者成名錄.yml',
  # '魔彈之王與戰姬.yml',
  # '魔彈之王與凍漣的雪姬.yaml',
  # '魔彈之王與聖泉的雙紋劍.yaml',
  # '怕痛.yml',
  # '地圖化.yml',
  
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
  # '靠神獸們成為世界最強吧.yaml',
  # '創始魔法師.yaml',
  # '幸存煉金術師的城市慢活記.yaml',
  # '軍武宅轉開軍隊後宮.yaml'
  '女兒已經升到了S級.yaml',
  
  # '田中～年齡等於單身資歷的魔法師～.yaml',
  # '世界最強後衛.yaml',
  # '鐵鏟無雙.yaml',
  # '被女神騙到異世界的我展開後宮生活.yaml',
  # '等級封頂的最強劍聖女碧翠斯也有弱點.yaml',
  # '因為不是真正的夥伴而被逐出勇者隊伍.yaml',
  # '勇者以想要成為朋友的視線看了過來！.yaml',
  # '孤單一人的異世界攻略.yaml',
  # '可以讀檔的旅店.yaml',
  # '帶著外掛轉生為公會櫃台小姐.yaml',
  # '輔助魔法與召喚魔法的選擇.yaml',

  # '無職轉生～到了異世界就拿出真本事～.yaml',
  # '刮掉鬍子的我與撿到的女高中生.yaml',
  # '我那轉生成魔導少女的雙劍實在太優秀了.yaml',
  # 'LDK與2JK～26歲上班族和兩名女高生的同居生活～.yaml',
  # '就算是有點色色的三姊妹，你也願意娶回家嗎.yaml',
  # '失格紋的最強賢者.yaml',
  # '精靈幻想記.yaml',
  ]
  for book_name in book_list:

    cwd = os.getcwd()
    print("book_name", book_name)
    config = ConfigHelper(config_name=book_name, config_path=os.path.join(cwd, 'books_yaml')).get_config()

    books = config['book']['books']
    book_info = config['book']['info']
    for book in books:
      print(book[0], book[1])
      main(book[0], book[1], book_info)