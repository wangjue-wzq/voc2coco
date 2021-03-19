import os
import numpy as np
import cv2
import tqdm
import random
from xml.dom.minidom import Document

def write2xml(xml_name,img_name,img_size,txt_list):
    doc = Document()
    annot = doc.createElement('annotation')
    doc.appendChild(annot)
    filename = doc.createElement('filename')
    filename_txt = doc.createTextNode(img_name)
    filename.appendChild(filename_txt)
    annot.appendChild(filename)

    source = doc.createElement('source')
    database = doc.createElement('database')
    database_txt = doc.createTextNode('DOTA')
    database.appendChild(database_txt)
    source.appendChild(database)
    annot.appendChild(source)

    size = doc.createElement('size')
    width = doc.createElement('width')
    width_txt = doc.createTextNode(str(img_size[0]))
    width.appendChild(width_txt)
    size.appendChild(width)
    height = doc.createElement('height')
    height_txt = doc.createTextNode(str(img_size[1]))
    height.appendChild(height_txt)
    size.appendChild(height)
    depth = doc.createElement('depth')
    depth_txt = doc.createTextNode(str(img_size[2]))
    depth.appendChild(depth_txt)
    size.appendChild(depth)
    annot.appendChild(size)

    segmented = doc.createElement('segmented')
    segmented_txt = doc.createTextNode('0')
    segmented.appendChild(segmented_txt)
    annot.appendChild(segmented)

    for idx_obj in txt_list:
        obj = doc.createElement('object')
        name = doc.createElement('name')
        name_txt = doc.createTextNode(idx_obj[4])
        name.appendChild(name_txt)
        obj.appendChild(name)
        pose = doc.createElement('pose')
        pose_txt = doc.createTextNode('Unspecified')
        pose.appendChild(pose_txt)
        obj.appendChild(pose)
        bndbox = doc.createElement('bndbox')
        xmin = doc.createElement('xmin')
        xmin_txt = doc.createTextNode(str(idx_obj[0]))
        xmin.appendChild(xmin_txt)
        bndbox.appendChild(xmin)
        ymin = doc.createElement('ymin')
        ymin_txt = doc.createTextNode(str(idx_obj[1]))
        ymin.appendChild(ymin_txt)
        bndbox.appendChild(ymin)
        xmax = doc.createElement('xmax')
        xmax_txt = doc.createTextNode(str(idx_obj[2]))
        xmax.appendChild(xmax_txt)
        bndbox.appendChild(xmax)
        ymax = doc.createElement('ymax')
        ymax_txt = doc.createTextNode(str(idx_obj[3]))
        ymax.appendChild(ymax_txt)
        bndbox.appendChild(ymax)
        diff = doc.createElement('difficult')
        diff_txt = doc.createTextNode(idx_obj[5])
        diff.appendChild(diff_txt)
        bndbox.appendChild(diff)
        obj.appendChild(bndbox)
        annot.appendChild(obj)

    # doc.writexml()
    with open(xml_name, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    return

def get_xml_anno():
    src_dir_img = '../data/DOTA/train/images/'
    src_dir_txt = '../data/DOTA/train/labelTxt-v1.0/label_horizon/'
    tar_dir_xml = '../data/DOTA/train/labelTxt-v1.0/label_horzion_xml/'
    fileList = os.listdir(src_dir_txt)
    # print(fileList)
    i = 0
    print('begin')
    for idx_path in tqdm.tqdm(fileList):
        txt_path = os.path.join(src_dir_txt,idx_path)
        xml_path = os.path.join(tar_dir_xml,idx_path.replace('.txt','.xml'))
        img = cv2.imread(src_dir_img+idx_path.replace('.txt','.png'))
        img_size = [0] * 3
        img_size[0], img_size[1], img_size[2] = img.shape
        file = open(txt_path)
        diagonal_file = []
        doc = Document()
        for data in file.readlines():
            diagonal = [0]*6
            coord_str = data.strip('\n').split(' ')
            # print(coord_str)
            coord = list(map(float, coord_str[:-2]))
            coord = list(map(int, coord))
            diagonal[0] = min(coord[0::2])
            diagonal[1] = min(coord[1::2])
            diagonal[2] = max(coord[0::2])
            diagonal[3] = max(coord[1::2])
            diagonal[4] = coord_str[-2]
            diagonal[5] = coord_str[-1]
            # file.write(str(diagonal)+'\n')
            diagonal_file.append(diagonal)
        # file.write(diagonal_file)
        # print(np.array(diagonal))
        # write2xml(xml_path,idx_path.replace('.txt','.png'),img_size,diagonal_file)
        write2xml(xml_path, idx_path.replace('.txt', '.png'), img_size, diagonal_file)
        file.close()

def get_txt_anno():
    # src_dir_img = '../data/DOTA_8/val800/images/images/'
    # src_dir_txt = '../data/DOTA_8/val800/images/labelTxt-v1.0/'
    # tar_dir_xml = '../data/DOTA_8/val800/images/label_xml/'
    # src_dir_img = '../data/DOTA_1/val1024/images/'
    # src_dir_txt = '../data/DOTA_1/small_obj/val1024/label_horizon/'
    # tar_dir_xml = '../data/DOTA_1/small_obj/val1024/Annotations/'
    src_dir_img = '../data/xView/train800/images/images/'
    src_dir_txt = '../data/xView/train800/images/labelTxt-v1.0/'
    tar_dir_xml = '../data/xView/train800/images/label_xml/'
    fileList = os.listdir(src_dir_txt)
    # print(fileList)
    fileList = tqdm.tqdm(fileList)
    for idx_path in fileList:
        txt_path = os.path.join(src_dir_txt,idx_path)
        xml_path = os.path.join(tar_dir_xml,idx_path.replace('.txt','x.xml'))
        img = cv2.imread(src_dir_img+idx_path.replace('.txt','.png'))
        img_size = [0] * 3
        img_size[0], img_size[1], img_size[2] = img.shape
        # img_size[0], img_size[1], img_size[2] = 1024, 1024, 3
        file = open(txt_path)
        diagonal_file = []
        doc = Document()
        for data in file.readlines():
            diagonal = [0]*6
            coord_str = data.strip('\n').split(' ')
            # print(coord_str)
            coord = list(map(float, coord_str[:-2]))
            coord = list(map(int, coord))
            diagonal[0] = min(coord[0::2])
            diagonal[1] = min(coord[1::2])
            diagonal[2] = max(coord[0::2])
            diagonal[3] = max(coord[1::2])
            diagonal[4] = coord_str[-2]
            diagonal[5] = coord_str[-1]
            # file.write(str(diagonal)+'\n')
            diagonal_file.append(diagonal)
        # file.write(diagonal_file)
        # print(np.array(diagonal))
        # write2xml(xml_path,idx_path.replace('.txt','.png'),img_size,diagonal_file)
        write2xml(xml_path, idx_path.replace('.txt', '.png'), img_size, diagonal_file)
        file.close()

def get_train_idx():
    src_dir_txt = '../data/DOTA_1/val1024/labelTxt-v1.0'
    out_path = '../data/DOTA_1/val1024/val_aug1_0.5.txt'
    fileList = os.listdir(src_dir_txt)
    list_img = []
    for idx in fileList:
        if idx.split('__')[1] == '1' or idx.split('__')[1] == '0.5':
            list_img.append(idx.strip('.txt'))

    list_img = np.array(list_img)
    # list_img = np.sort(list_img)
    np.savetxt(out_path, list_img,fmt = '%s')

def select_trainval_test(src_xmlpath,ratio,train_name,test_name):
    xml_list = os.listdir(src_xmlpath)
    random.shuffle(xml_list)
    xml_list = [xml[:-4] for xml in xml_list]
    ratio = round(len(xml_list)*ratio)
    train_list = np.array(xml_list[:ratio]).reshape(-1,1)
    test_list = np.array(xml_list[ratio:]).reshape(-1,1)
    np.savetxt(train_name,train_list,fmt='%s')
    np.savetxt(test_name,test_list,fmt='%s')

# get_train_idx()
# get_txt_anno()
# get_xml_anno()
src_xmlpath = '/data2/datasets/small_obj/annotation/label_p_v_s_100/'
ratio = 0.5
train_name = '/data2/datasets/small_obj/train/train_pvs100.txt'
test_name = '/data2/datasets/small_obj/test/test_pvs100.txt'
# select_trainval_test(src_xmlpath,ratio,train_name,test_name)
DIOR_except_pvs_without_null = '/data2/datasets/small_obj/extra_dataset/DIOR_except_pvs/excpet_pvs_MSM_anno_without_null/'
dior_pvs_without_null = os.listdir(DIOR_except_pvs_without_null)
dior_pvs_without_null = [name.strip('.xml') for name in dior_pvs_without_null]
dior_pvs_without_null = np.array(dior_pvs_without_null).reshape(-1,1)
np.savetxt('/data2/datasets/small_obj/extra_dataset/DIOR_except_pvs/'+'train_dior_pvs_without_null.txt',dior_pvs_without_null,fmt='%s')