#coding: utf-8
'''
Created on 2016年4月17日

@author: Shawn Wang

@email: 744585345@qq.com

'''
import pickle
import struct


class Node:
    '''哈夫曼树节点类'''
    def __init__(self, value = "", left= None, right = None, frequency = 0, code=''):
        self.value = value
        self.left = left
        self.right = right
        self.frequency = frequency
        #存储该节点的编码
        self.code = code


def give_code(node):
    ''' 对节点进行编码 '''
    if node.left:
        node.left.code = "%s%s" % (node.code, "0")
        give_code(node.left)
    if node.right:
        node.right.code = "%s%s" % (node.code, "1")
        give_code(node.right)
        
def save_code(huff_map, node):
    '''将哈夫曼码存储到字典中'''
    
    #遍历到孩子节点
    if not node.left and not node.right:
        huff_map[node.value] = node.code
    if node.left:
        save_code(huff_map, node.left)
    if node.right:
        save_code(huff_map, node.right)
    
def test_give_code(node):
    ''' 测试编码函数 '''
    #遍历到了孩子节点
    if not node.left and not node.right:  
        print "%s %s" % (node.value, node.code)  
    if node.left:  
        test_give_code(node.left)  
    if node.right:  
        test_give_code(node.right)  

def change_value_to_key(huffmap):
    '''将键值转换为键'''
    my_map = dict()
    for (key, value) in huffmap.items():
        my_map[value] = key
        
    return my_map

def count_letter(file_path):
    ''' 
    *统计文本中的字符个数 
    *返回字典和源字符串
     '''
    letter_map = dict()
    #存储原始字符串
    origin_data = ''
    with open(file_path) as f:
        for line in f.readlines():
            origin_data += line
            for letter in line:
                #查询字典， 如果字符已经存在就+1 ，否则添加该键并键值+1
                letter_map[letter] = letter_map.get(letter, 0) + 1
##    #test code
##    print letter_map
##    print origin_data
    return letter_map, origin_data

def create_node_list(letter_map):
    ''' 
        *将字符-频率字典转换为节点列表 
        *返回值为节点列表
    '''
    node_list = list()
    
    for(key, frequency) in letter_map.items():
        #创建节点
        node = Node(value = key, frequency = frequency)
        #往列表中添加节点
        node_list.append(node)
    #将节点列表按字符的频率排序
    node_list.sort(cmp= lambda x, y: cmp(x.frequency, y.frequency))
    return node_list

def create_huff_tree(node_list):
    ''' 
        *创建哈夫曼树 
        *返回哈夫曼树的树根
    '''
    for i in xrange(len(node_list) - 1):
        node1 = node_list[0]  
        node2 = node_list[1]  
        node = Node()  
        node.left = node1  
        node.right = node2  
        node.frequency = node1.frequency + node2.frequency  
        node_list[0] = node  
        node_list.pop(1)  
        node_list.sort(cmp=lambda n1, n2: cmp(n1.frequency, n2.frequency))
    
    return node_list[0] 

def build_huff_code_data(origin_data, huff_map):
    code_data = ''
    for letter in origin_data:
        code_data += huff_map[letter]
    return code_data

def store_file(file_path, huff_map, code_data):
    '''
        *写二进制文件
    '''
    try:
        file_handler = open("%s.hfz" % file_path, "wb")
        
        #借助picke将字典转换为二进制字符串
        huff_map_bytes = pickle.dumps(huff_map)
        print huff_map_bytes, "-----------------"
        #在文件头部存储字典字节流的长度
        file_handler.write(struct.pack("I", len(huff_map_bytes)))
        print struct.pack("I", len(huff_map_bytes)) , "-----------------"
        #将字典作为一个字符串写入文件头
        file_handler.write(struct.pack("%ds" % len(huff_map_bytes), huff_map_bytes))
        print struct.pack("%ds" % len(huff_map_bytes), huff_map_bytes), "-----------------"
        #在文件头部写入文本二进制流的字节长度
        file_handler.write(struct.pack("B", len(code_data) % 8))
        print struct.pack("B", len(code_data) % 8), "-----------------"
        #字节流的字节数
        length = len(code_data)
        for i in xrange(0, length, 8):
            if i + 8 < length:
                file_handler.write(struct.pack("B", int(code_data[i : i+8], 2)))
            else:
                file_handler.write(struct.pack("B", int(code_data[i:], 2)))
    except Exception as e:
        print e
    finally:
        file_handler.close()
def decompress(file_path):
    '''
    *解码
    '''
	
    file_handler = open(file_path)
        #读取编码字典长度
    size = struct.unpack("I", file_handler.read(4))[0]
        #还原码表字典
    huff_map = pickle.loads(file_handler.read(size))
        #读取字符流长度       
    left = struct.unpack("B", file_handler.read(1))[0] 
        
        #先读一个内容字节
    data = file_handler.read(1)
        
    data_list = []
        #继续读完内容字节
    while data != '':
            #将二进制数据还原为十进制的哈夫曼编码
        bin_data = bin(struct.unpack("B", data)[0])[2 : ]
        data_list.append(bin_data)
        data = file_handler.read(1)
    

    file_handler.close()
        
    for i in xrange(len(data_list) - 1):
        data_list[i] = "%s%s" % ('0' * (8 - len(data_list[i])), data_list[i])
    data_list[-1] = "%s%s" % ('0' * (left - len(data_list[-1])), data_list[-1])
    
    encode_data = ''.join(data_list)
    current_code = ''
    huff_map = change_value_to_key(huff_map)
    file_handler = open("%s_orig" % file_path, "w")
    for letter in encode_data:
        current_code += letter
        if huff_map.get(current_code):
            file_handler.write(huff_map[current_code])
            current_code = ''
    file_handler.close()
    
    print "finish"
