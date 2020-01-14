# WebControl
* 最簡指令
    * window_maximize  
    * browser_url  
    * get_element_tree  
    * window_screen_shot  
    * switch_to_iframe  
    * switch_to_parent_frame  
    * find_element  
    * browser_pagination  
    * switch_to_another_window  
    * create_new_tab  
    * btn_click  
    * get_css_attribute  
    * get_element_size  
    * scroller_slip_to  
    * close_pagination  
    * get_current_url  
    * get_current_title  
    * get_element_text  
    * element_typing  
    * element_wait  
* 複雜指令
    * xpath_click<br>
    點擊指定的xpath元件
    * xpath_select_option<br>
    透過xpath選取特定的值
    * xpath_text<br>
    取得指定xpath元件的html顯示文字
    * xpath_is_selected<br>
    查看 xpath 元件是否被選取
    * xpath_value<br>
    取得xpath元件的數值(input , textarea)
    * xpath_send_keys<br>
    對xpath元件輸入值
    * xpath_swich_iframe<br>
    切換到指定xpath的iframe, 並檢查網址是否正確

# exceptions<br>
Web control有Error時,透過Exceptions去整理Error
* ElementNotFoundException<br>
 當元件找不到所使用