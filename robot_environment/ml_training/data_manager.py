import random
import shutil
from shutil import copyfile
import os


def create_train_test_dirs(root_path, category, type):
    os.makedirs(os.path.join(root_path, category, type))


def split_data(SOURCE, TRAINING, TESTING, SPLIT_SIZE):
    images = os.listdir(SOURCE)
    for img in images:
        if os.path.getsize(os.path.join(SOURCE, img)) == 0:
            print(img, " is zero length, so ignoring.")
            images.remove(img)

    print(len(images))

    split_val = int(len(images) * SPLIT_SIZE)
    random.shuffle(images)

    for train_img in images[:split_val]:
        copyfile(os.path.join(SOURCE, train_img), os.path.join(TRAINING, train_img))

    for test_img in images[split_val:]:
        copyfile(os.path.join(SOURCE, test_img), os.path.join(TESTING, test_img))


root_dir = "./ml/hand_gestures_dataset"

if os.path.exists(root_dir):
    shutil.rmtree(root_dir)

source_path = './hand_gestures_dataset'
source_path_sub = []

k = 0
for i in ['0', '1', '2', '3']:
    source_path_sub.append(os.path.join(source_path, i))
    print(f'There are {len(os.listdir(source_path_sub[k]))} images of {i}')
    k += 1

for j in range(4):
    os.makedirs(os.path.join(root_dir, "training", str(j)))
    os.makedirs(os.path.join(root_dir, "testing", str(j)))
    split_data(source_path_sub[j], os.path.join(root_dir, "training", str(j)),
               os.path.join(root_dir, "testing", str(j)), .9)
