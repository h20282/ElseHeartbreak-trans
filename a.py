import os
import csv
import glob
import re
import requests
import pyperclip

all_files = glob.glob("English/*.mtf")


pyperclip.copy('The text to be copied to the clipboard.')
pyperclip.paste()   # 'The text to be copied to the clipboard.'
print(f"我是复制的内容：{pyperclip.paste()}")


all_trans = []

for per_file in all_files:
    for line in open(per_file, encoding='utf-8'):
        line = line.strip()
        match = re.match(r'"(.*?)"\s*=>\s*"(.*?)"', line)
        if match:
            swedish = match.group(1)
            english = match.group(2)
            
            all_trans.append({'file': per_file, 'swedish': swedish, 'english': english, 'chinese': ''})
        else:
            raise Exception('invalid line: `{}`'.format(line))
        
print(all_trans)

start_pos = 0
txt = ''
while(start_pos < len(all_trans)):
    i = start_pos
    while len(txt) < 4900:
        txt = txt + all_trans[i]['swedish'] + '\n'
        i = i+1
        if (i>=len(all_trans)):
            break
    txt = txt.strip()
    pyperclip.copy(txt)
    print('{} copyed'.format(txt))

    while pyperclip.paste()==txt or len(pyperclip.paste().split('\n')) != i-start_pos :
        pyperclip.copy(txt)
        print('goto translate it, {}/{}'.format(i, len(all_trans)))
        input()
    txt = ''

    chinese_trans = pyperclip.paste().split('\n')
    print('{} getted, fill it'.format(chinese_trans))
    input()
    for j in range(len(chinese_trans)):
        if (start_pos+j >= len(all_trans)):
            break
        all_trans[start_pos+j]['chinese'] = chinese_trans[j]
        print('{} -> {}'.format(all_trans[start_pos+j]['swedish'], all_trans[start_pos+j]['chinese']))
    input()

    start_pos = i


with open('a.csv', 'w', encoding='utf-8') as f:
    csv_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(['file', 'swedish', 'english', 'chinese'])
    for per_trans in all_trans:
        csv_writer.writerow([per_trans['file'], per_trans['swedish'], per_trans['english'], per_trans['chinese']])
