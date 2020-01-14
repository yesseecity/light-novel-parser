class ElementNotFoundException(Exception):
    def __init__(self, dom_id=None, class_name=None, xpath=None, msg=None, mode=None, wait_time=None):
        self.dom_id = dom_id
        self.class_name = class_name
        self.xpath = xpath
        self.mode = mode
        self.wait_time = wait_time
        self.msg = msg
        # TODO  找不到元件時的 error追蹤

    def __str__(self):
        exception_msg = "Error: 元件 %s 找不到\n" % self.msg
        return exception_msg
