from ebooklib import epub

book = epub.EpubBook()

# set metadata
book.set_title('OVERLORD-第十二卷 聖王國的聖騎士 上')
book.set_language('zh-tw')

book.add_author('丸山くがね')

# create chapter
c1 = epub.EpubHtml(title='第一章', file_name='chap_01.xhtml')
content = '<h1>第一章 魔皇亞達巴沃</h1><p>洛布爾聖王國以裏．耶斯提傑王國西南方的半島為領土。<br\>該國擁立行使信仰係魔法的聖王為君，君主與神殿勢力和睦治國，是個宗教色彩濃厚的國度，話雖如此，程度倒還不比斯連教國。<br\>具有這幾項特色的洛布爾聖王國，國土上有兩點特別稀奇。<br\>一個是國土被大海分為南北兩地。當然，國土並未完全遭到分割，而是環抱一個巨大海灣──縱長約莫四十公裏，橫寬長達兩百公裏──形成U字橫擺的國土形狀。<br\>因此甚至有人稱兩地為北聖王國與南聖王國。<br\>另外還有一個特色。<br\>就是在半島入口處，建造了橫貫南北，全長超過一百公裏的長城。<br\>這是為了阻擋居住於聖王國東側與斯連教國之間丘陵地帶的多種亞人類部落進犯疆土。<br\>耗費大量歲月與國力建設的厚重雄偉的長城，述說著亞人類的存在讓聖王國遭受過多少苦難與悲劇。<br\>亞人類與人類，在能力上有著極大落差。<br\>的確，哥布林等部分亞人類比人類脆弱也是事實。<br\>他們個頭比人類矮，就體能、智能與魔法吟唱者（Magic Caster）誕生的比例等等而論，都是劣於人類的種族。<br\>但縱然是不如人類的哥布林，隻要活用夜間視力與容易藏身隱蔽處的矮小體格──例如夜晚森林戰鬥的奇襲──對人類而言肯定成為棘手敵人。<br\>況且許多亞人類擁有比人類更強韌的肉體，更有不少種族具有先天性魔法能力。一旦容許亞人類入侵國境，擊退敵軍所需付出的代價將會是大量鮮血。</p>'
c1.content = content.encode()

c2 = epub.EpubHtml(title='第二章', file_name='chap_02.xhtml')
content = '<h1>第二章 尋求救援</h1>況且許多亞人類擁有比人類更強韌的肉體，更有不少種族具有先天性魔法能力。一旦容許亞人類入侵國境，擊退敵軍所需付出的代價將會是大量鮮血。<br\>正因為如此，聖王國才會加強防禦。<br\>為了不讓亞人類踏進這片國土一步。<br\>為了讓亞人類知道這塊家園並不屬於他們。<br\>為了告訴他們隻要敢越雷池一步，我軍將抵死不從，奮勇抗敵。<br\>就這樣，長城蓋了起來，但它有它的問題存在。<br\>若要讓長城隨時保持在最佳狀態，龐大兵力常年駐守將在所難免。過去聖王國的首腦陣容曾經試算過，在亞人類的一個部落攻打過來時，需要預備多少兵力才能戰勝。<br\>結果是：不用等亞人類攻進國境，國家就先破產了。<br\>國內沒有餘力組織多餘流動兵力，但有必要布署數量足夠的兵員。</p>'
c2.content = content.encode()


# add chapter
book.add_item(c1)
book.add_item(c2)



# define Table Of Contents
book.toc = (
  epub.Link('chap_01.xhtml', u'第一章', 'ch-1'),
  epub.Link('chap_02.xhtml', u'第二章', 'ch-2'),
  # (epub.Section('Simple book'), (c1, c2, ) )
)

# add cover image
book.set_cover("image.jpg", open('12.jpg', 'rb').read())

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# # define CSS style
# style = 'BODY {color: white;}'
# nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# # add CSS file
# book.add_item(nav_css)

# basic spine
# 把書訂起來
book.spine = ['nav', c1, c2]

# write to the file
epub.write_epub('test.epub', book, {})