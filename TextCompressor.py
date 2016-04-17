#coding: utf-8
'''
Created on 2016年4月17日

@author: Shawn Wang

@email: 744585345@qq.com

'''
from util import *
def compress(file_path):
    
    (letter_map, origin_data) = count_letter(file_path)
    
    node_list = create_node_list(letter_map)
    
    huff_tree = create_huff_tree(node_list)
    
    give_code(huff_tree)
    
    huff_map = {}
    save_code(huff_map, huff_tree)
    
    code_data = build_huff_code_data(origin_data, huff_map)
    
    store_file(file_path, huff_map, code_data)
    print "compress"
    

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