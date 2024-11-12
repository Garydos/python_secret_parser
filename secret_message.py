from html.parser import HTMLParser
import urllib.request

class SecretTableParser(HTMLParser):
    def __init__(self):
        self.in_table = False
        self.current_position = 0
        self.skip_header = 0
        self.data = []
        self.current_x = 0
        self.current_y = 0
        self.y_max = 0
        self.current_char = ''
        super().__init__()
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
            self.data.sort(key=lambda entry: 0 - int(entry[0]) * 100 + int(entry[1]))
    def handle_data(self, data):
        if self.in_table:
            if self.skip_header < 3:
                self.skip_header += 1
                return
            if self.current_position == 0:
                self.current_x = int(data)
            elif self.current_position == 1:
                self.current_char = data
            elif self.current_position == 2:
                self.current_y = int(data)
            self.current_position += 1
            if self.current_position > 2:
                self.current_position = 0
                self.data.append((self.current_y, self.current_x, self.current_char))
                if self.current_y > self.y_max:
                    self.y_max = self.current_y

def printTable(data, y_max):
    current_string = ""
    current_y = y_max
    current_x = 0
    for entry in data:
        if current_y > entry[0]:
            current_y = entry[0]
            print(current_string)
            current_string = ""
            current_x = 0
        while current_x < entry[1]:
            current_string = current_string + " "
            current_x = current_x + 1
        current_string = current_string + entry[2]
        current_x += 1
    if current_string != "":
        print(current_string)

def decodeMessage(url):
    http_request = urllib.request.urlopen(url)
    raw_html = http_request.read().decode('utf-8')
    parser = SecretTableParser()
    parser.feed(raw_html)
    #print(parser.data)
    #print(len(parser.data))
    #print(parser.y_max)
    printTable(parser.data, parser.y_max)

if __name__ == "__main__":
    decodeMessage("https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub")