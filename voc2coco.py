# coding=utf-8
import os
import json
import tqdm
import xml.etree.ElementTree as ET

dior_clses = ['airplane', 'airport', 'baseballfield', 'basketballcourt',
           'bridge', 'chimney', 'dam', 'Expressway-Service-area',
           'Expressway-toll-station', 'harbor', 'golffield',
           'groundtrackfield', 'overpass', 'ship', 'stadium',
           'storagetank', 'tenniscourt', 'trainstation', 'vehicle', 'windmill'
           ]

dior_clses_except_pvs = ['airport', 'baseballfield', 'basketballcourt',
           'bridge', 'chimney', 'dam', 'Expressway-Service-area',
           'Expressway-toll-station', 'harbor', 'golffield',
           'groundtrackfield', 'overpass', 'stadium',
           'storagetank', 'tenniscourt', 'trainstation', 'windmill']

dota_clses = ['plane', 'baseball-diamond',
           'bridge', 'ground-track-field',
           'small-vehicle', 'large-vehicle',
           'ship', 'tennis-court',
           'basketball-court', 'storage-tank',
           'soccer-ball-field', 'roundabout',
           'harbor', 'swimming-pool',
           'helicopter']

small_obj_name_dota_dior_xView = ['large-vehicle', 'plane', 'ship','small-vehicle',
                          'airplane','ship', 'vehicle', 'Fixed-wing-Aircraft',
                          'Small-Aircraft','Cargo-Plane','Passenger-Vehicle',
                          'Small-Car','Bus','Maritime-Vessel','Motorboat',
                          'Sailboat','Tugboat','Barge','Fishing-Vessel','Ferry',
                          'Yacht','Container-Ship','Oil-Tanker']


dota_clses_small = ['plane','small-vehicle','large-vehicle','ship']


def getimages(xmlname, categories, id,min_size=None,max_size=None):
    sig_xml_box = []
    tree = ET.parse(xmlname)
    root = tree.getroot()
    images = {}
    for i in root:  # travers the first root
        if i.tag == 'filename':
            file_name = i.text  # 0001.jpg
            # print('image name: ', file_name)
            images['file_name'] = file_name
        if i.tag == 'size':
            for j in i:
                if j.tag == 'width':
                    width = j.text
                    images['width'] = width
                if j.tag == 'height':
                    height = j.text
                    images['height'] = height
        if i.tag == 'object':
            for j in i:
                if j.tag == 'name':
                    cls_name = j.text
                if cls_name not in categories:
                    print(cls_name + 'is not in' + str(categories))
                    # ValueError(cls_name + 'is not in' + str(categories))
                    continue
                cat_id = categories.index(cls_name) + 1
                if j.tag == 'bndbox':
                    bbox = []
                    xmin = 0
                    ymin = 0
                    xmax = 0
                    ymax = 0
                    for r in j:
                        if r.tag == 'xmin':
                            xmin = eval(r.text)
                        if r.tag == 'ymin':
                            ymin = eval(r.text)
                        if r.tag == 'xmax':
                            xmax = eval(r.text)
                        if r.tag == 'ymax':
                            ymax = eval(r.text)
                    bbox.append(xmin)
                    bbox.append(ymin)
                    bbox.append(xmax - xmin)
                    bbox.append(ymax - ymin)
                    bbox.append(id)   # save the image_id of current box
                    bbox.append(cat_id)
                    area = (xmax - xmin) * (ymax - ymin)
                    if min_size is not None and area < min_size:
                        continue
                    if max_size is not None and area > max_size:
                        continue
                    bbox.append((xmax - xmin) * (ymax - ymin))   # bbox's area
                    sig_xml_box.append(bbox)
                    # print('bbox', xmin, ymin, xmax - xmin, ymax - ymin, 'id', id, 'cls_id', cat_id)
    images['id'] = id
    # print ('sig_img_box', sig_xml_box)
    return images, sig_xml_box

def txt2list(txtfile):
    f = open(txtfile)
    l = []
    for line in f:
        l.append(line[:-1])
    return l

def xml2json(xml_path,xml_names,categories,json_name,max_size=None):
    xmls = []
    bboxes = []
    ann_js = {}

    for ind, xml_name in enumerate(xml_names):
        xmls.append(os.path.join(xml_path, xml_name ))
    images = []
    xmls = tqdm.tqdm(xmls)
    for i_index, xml_file in enumerate(xmls):
        image, sig_xml_bbox = getimages(xml_file, categories, i_index,max_size=max_size)
        images.append(image)
        bboxes.extend(sig_xml_bbox)
    ann_js['images'] = images
    ann_js['categories'] = categories
    annotations = []
    print(len(bboxes))
    bboxes = tqdm.tqdm(bboxes)
    for box_ind, box in enumerate(bboxes):
        anno = {}
        anno['image_id'] =  box[-3]
        anno['category_id'] = box[-2]
        anno['bbox'] = box[:-3]
        anno['id'] = box_ind
        anno['area'] = box[-1]
        anno['iscrowd'] = 0
        annotations.append(anno)
    ann_js['annotations'] = annotations
    json.dump(ann_js, open(json_name, 'w'), indent=4)  # indent=4 更加美观显示



# voc2007xmls = 'anns'
# voc2007xmls = '/data2/datasets/DIOR/Annotations'
# dior_xmls = '/data2/datasets/DIOR/Annotations'
# dior_xmls = '/data2/datasets/DOTA/train/labelTxt-v1.0/label_horizon_xml'
# dior_select_xml = '/data2/datasets/small_obj/train/label_dior'
dior_select_xml = '/data2/datasets/small_obj/train/label_dior'
# test_txt = 'voc2007/test.txt'
# test_txt = '/data2/chenjia/data/VOCdevkit/VOC2007/ImageSets/Main/test.txt'
test_txt = '/data2/datasets/DIOR/ImageSets/Main/trainval.txt'
json_name_dior = '/data2/datasets/DIOR/ImageSets/Main/dior_small_coco.json'
json_name_dota = '/data2/datasets/DOTA/train/labelTxt-v1.0/dota_small_coco.json'
json_name_dior_test = '/data2/datasets/small_obj/train/dior_train.json'

dota_select_train = '/data2/datasets/small_obj/label_all/label_small_xml'
# json_name = '/data2/datasets/small_obj/annotation/label_p_v_s.json'
# json_name = '/data2/datasets/small_obj/extra_dataset/DIOR_except_pvs/except_MSM_p_v_s.json'
json_name = '/data2/datasets/small_obj/annotation/pvs_large_96.json'
# small_pvs = '/data2/datasets/small_obj/annotation/label_p_v_s_100'
# except_small_pvs = '/data2/datasets/small_obj/extra_dataset/DIOR_except_pvs/except_pvs_annotation'
except_small_pvs = '/data2/datasets/small_obj/annotation/label_p_v_s_large96/'

small_clses = ['plane','vehicle','ship']
dior_clses_small = ['airplane', 'ship','vehicle']
clses_name = small_clses
select_xml = except_small_pvs
categories = []
for iind, cat in enumerate(clses_name):
    cate = {}
    cate['supercategory'] = cat
    cate['name'] = cat
    cate['id'] = iind
    categories.append(cate)

train_file_idx = open('/data2/datasets/small_obj/train/train_pvs100.txt')
# xml_names = train_file_idx.readlines()
# xml_names = [name.strip('\n')+'.xml' for name in xml_names]
xml_names = os.listdir(except_small_pvs)
xml2json(select_xml,xml_names,clses_name,json_name,max_size=None)