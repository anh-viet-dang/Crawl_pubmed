from lib import send_request



"""
Từ pmid đã có, thực hiện tìm pmid similar, cited, reference
if tìm xem trong list pmid gene/not gene đã có chưa, nếu có:
    bỏ qua
elif classfication (title, abstract):
    liên quan đến gen 
        -> đưa qua queue download
        -> them vào pmid gene
        -> search tiếp similar, cited, ref để lấy pmid, title, abstract
    ko liên quan đến gen 
        -> add vào not gene

# search theo hường BFS, build graph search, tránh recursive
# lần đầu download theo hướng liên quan đến gene trước
"""