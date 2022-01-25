from googletrans import Translator

def read_F1text(path:str) -> list:
    # https://s-nako.work/2020/06/unicodedecodeerror-cp932-codec-cant-decode-byte-0x99-in-position-illegal-multibyte-sequence/
    with open(path, 'r', encoding='utf_8') as f:
        lines = f.read().split('\n')
    return lines[:-1]


def write_translate(
    lines:list,     # danh sach các dòng
    path:str,       # path để viết file đã dịch
    num_line:int    # dòng đã dịch xong
    ) -> None:

    translator = Translator()
    fw = open(path, 'a', encoding= 'utf_8')
    ff = open("tranF1_fail.txt", 'a', encoding= 'utf_8')

    for i, line in enumerate(lines):
        if i < num_line: continue
        print(i+1,' -> ' ,line)
        tag = i%4
        if tag == 0: # pmid
            fw.write(line.strip() + '\n')

        elif tag == 1: # dòng title
            try:
                dich = translator.translate(line.strip(), src='en', dest='vi')
                fw.write(dich.text.strip() + '\n')
            except Exception as e:
                print(e)
                fw.write('\n')
                ff.write(lines[i-tag].strip() + '\n')   # viết lại pmid

        elif tag == 2: # dòng abstract
            if line != '':
                try:
                    dich = translator.translate(line.strip(), src='en', dest='vi')
                    fw.write(dich.text.strip() + '\n')
                except Exception as e:
                    print(e)
                    fw.write('\n')
                    ff.write(lines[i-tag].strip() + '\n')# viết lại pmid
            else:
                fw.write('\n')

        else:   # tag == 3  # dòng ngăn cách giữa 2 paper
            fw.write('\n')
    
    
    fw.close(); ff.close()



# __main__
""" số dòng bắt đầu từ 1
    (số dòng trong file txt - 1) % 4 == 0 là dòng pmid

    lấy số dòng pmid ngay phía trên + 4 - 1 là ra số num
    >>> num = số dòng pmid + 4 = 1

    >>> xóa hết nội dung tại dòng num + 1 
    >>> dòng num + 1 là dòng cuối cùng của file txt
"""
lines = read_F1text('/content/gdrive/MyDrive/Crawl_pubmed/data/similarF1.txt')

num = 228576        # phải viết hàm tính num dựa trên số dòng thay vì làm thủ công

write_translate(lines, "/content/gdrive/MyDrive/Crawl_pubmed/data/tran_similarF1.txt", num)