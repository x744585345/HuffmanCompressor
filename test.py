from util import *

def compress_test():
    ##    func cout_leter done
    (letter_map, origin_data) = count_letter("unit.txt")
##    print letter_map
##    print origin_data
##    create_node_list done
    node_list = create_node_list(letter_map)
##    for node in node_list:
##        print node.value, node.frequency
##
    #done
    huff_tree = create_huff_tree(node_list)
    #done
    give_code(huff_tree)
##    #done
##    test_give_code(huff_tree)

    huff_map = {}
    #done
    save_code(huff_map, huff_tree)    
##    print huff_map
    #done
    code_data = build_huff_code_data(origin_data, huff_map)
##    print code_data
    store_file("unit.txt", huff_map, code_data)
    print "done"

def decompress_test():
    decompress("unit.txt.hfz")

if __name__ == "__main__":
    decompress_test()
