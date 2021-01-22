import os
import sys
from glob import glob
import numpy as np
import cv2
import mrcnn.model as modellib
from utils.mrcnn_config import InferenceConfigMulti
from utils import signal_handler as sh
import mrcnn_config as cfg
import json


batch_size = 4


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_unprocessed_videos(video_list, dest_dir):
    ret_list = []
    print('Removing processed videos (initially: %d videos) ...' % len(video_list))
    for video_file in video_list:
        video_name = os.path.splitext(os.path.split(video_file)[1])[0]
        if not os.path.exists(os.path.join(dest_dir, video_name + '.json')):
            ret_list.append(video_file)
    print('Done. Found %d videos to process.' % len(ret_list))
    return ret_list


def main():
    config = InferenceConfigMulti()
    config.display()
    model = modellib.MaskRCNN(mode="inference", model_dir='', config=config)
    model.load_weights(cfg.weights_file, by_name=True)

    create_dir(cfg.bbox_dir)

    file_list = glob('%s/mp4/*' % cfg.dataset_dir)
    file_list = get_unprocessed_videos(file_list, cfg.bbox_dir)

    print('Procesing videos ...')
    for vid_num, videofile in enumerate(file_list):
        # Create output subdirectories
        videopath, file_name = os.path.split(videofile)
        print('Processing video "%s" (#%d of %d) ...' % (file_name, vid_num + 1, len(file_list)))
        json_filename = os.path.join(cfg.bbox_dir, os.path.splitext(file_name)[0] + '.json')

        # Open video capture from mp4 file
        video = cv2.VideoCapture(videofile)
        video_length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        batches = [batch_size] * (video_length//batch_size)
        batches.append(video_length % batch_size)

        vid_frame = 0
        bbox_dict = {}
        for this_batch in batches:

            images = []
            for i in range(this_batch):
                ret, bgr = video.read()
                # HACK: cv2 loads BGR, skimage loads RGB (expected by net).
                img = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                images.append(img)

            # Run detection
            results = model.detect(images, verbose=0)

            # Visualize results
            for i in range(this_batch):
                bboxes_frame = []
                r = results[i]
                for id in range(len(r['class_ids'])):
                    if r['class_ids'][id] == 1:  # 1 == 'person' class.
                        score = r['scores'][id]
                        y0, x0, yf, xf = tuple(r['rois'][id])
                        x, y, w, h = int(x0), int(y0), int(xf-x0), int(yf-y0)
                        # cv2.rectangle(img, (x0,y0), (xf,yf), color=(0,255,0), thickness=2)
                        bboxes_frame.append({"score": float(score), "rect": [x, y, w, h]})
                # cv2.imshow('image', img)
                # cv2.waitKey(1)
                bbox_dict['%06d' % vid_frame] = bboxes_frame
                vid_frame += 1

            pct = int(100 * (vid_frame/video_length))
            vpct = 100 * ((vid_num+1)/len(file_list))
            sys.stdout.write('\rVideo %06d, Frame %06d/%06d [%3d%%] ... %3.2f%% ' % (vid_num+1, vid_frame, video_length, pct, vpct))

            if not sh.work:
                print('Gracefully STOPPED.')
                sys.exit(0)

        fh = open(json_filename, 'w')
        json.dump(bbox_dict, fh)
        fh.close()
        print('Done.')

    print('Done.')


if __name__ == '__main__':
    main()
