#coding: utf-8
'''
Created on 2016年4月17日

@author: Shawn Wang

@email: 744585345@qq.com

'''
from util import *
def compress(file_path):
    #字符统计字典， 原始数据
    (letter_map, origin_data) = count_letter(file_path)
    #节点列表
    node_list = create_node_list(letter_map)
    #哈弗曼树根
    huff_tree = create_huff_tree(node_list)
    #进行哈弗曼编码
    give_code(huff_tree)

    #存储码表
    huff_map = {}
    save_code(huff_map, huff_tree)
    #哈弗曼编码后的数据
    code_data = build_huff_code_data(origin_data, huff_map)
    #写文件
    store_file(file_path, huff_map, code_data)
    print "compress"
def decompress(file_path):
    pass

mode = int(raw_input("Please input the mode number (0 for compress, 1 for decompress): "))

if(mode == 0):
    file_path = raw_input("Please input the file path:")
    compress(file_path)
    print "Accomplish the compression."
elif(mode == 1):
    file_path = raw_input("Please input the file path:")
    decompress(file_path)
    print "Accomplish the decompression."
else:
    print "Bad type please try again"
    raw_input("Press anykey to exit.")
    exit()
