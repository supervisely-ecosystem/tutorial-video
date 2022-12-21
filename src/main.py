import os
from shutil import rmtree

from dotenv import load_dotenv
import supervisely as sly
from supervisely.project.project_type import ProjectType

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

WORKSPACE_ID = int(os.environ["context.workspaceId"])

original_dir = "src/videos/original"
result_dir = "src/videos/result"

# remove the results directory if it exists
if os.path.exists(result_dir):
    rmtree(result_dir)
os.mkdir(result_dir)

# Create the new project
project = api.project.create(
    WORKSPACE_ID, "Animals", type=ProjectType.VIDEOS, change_name_if_conflict=True
)

# Create new datasets
dataset = api.dataset.create(project.id, "Birds", change_name_if_conflict=True)
dataset_2 = api.dataset.create(project.id, "Birds_2", change_name_if_conflict=True)

# Upload the video from the direcory to the new dataset
penguins_local_path = os.path.join(original_dir, "Penguins.mp4")
meta = {"my-field-1": "my-value-1", "my-field-2": "my-value-2"}

video_info = api.video.upload_path(
    dataset.id,
    name="Penguins",
    path=penguins_local_path,
    meta=meta,  # optional: you can add metadata to the video
)


# Get video info by id
id = video_info.id
video_info = api.video.get_info_by_id(id)


# Upload the video using hash to the another dataset
hash = video_info.hash
name = "Penguins_2"
penguins_info = api.video.upload_hash(dataset_2.id, name, hash)


# Upload a list of videos from the directory
names = ["Flamingo.mp4", "Swans.mp4", "Toucan.mp4"]
paths = [os.path.join(original_dir, name) for name in names]

# This method helps optimize code because it uses fewer queries to a Supervised database
upload_info = api.video.upload_paths(dataset.id, names, paths)


# Get a list of all videos in the dataset
video_info_list = api.video.get_list(dataset.id)


# Upload a list of videos by hashe to the another dataset
hashes, names, metas = [], [], []
# Create lists of hashes, videos names and meta information for each video
for video in video_info_list:
    hashes.append(video.hash)
    # It is necessary to upload videos with the same names(extentions) as in src dataset
    names.append(video.name)
    metas.append({video.name: video.frame_height})  # optional: you can add metadata

# This method helps optimize code because it uses fewer queries to a Supervised database
new_videos_info = api.video.upload_hashes(dataset_2.id, names, hashes, metas)


# Download the video by id to the local path
save_path = os.path.join(result_dir, f"{video_info.name}.mp4")
api.video.download_path(video_info.id, save_path)


# Download the frame of the video
frame_idx = 15
file_name = "frame.png"
save_path = os.path.join(result_dir, file_name)
api.video.frame.download_path(video_info.id, frame_idx, save_path)


# Download the range of video frames as images
frame_indexes = [5, 10, 20, 30, 45]
save_paths = [os.path.join(result_dir, f"frame_{idx}.png") for idx in frame_indexes]

# This method uses fewer queries to a Supervised database, helps to optimize your code
api.video.frame.download_paths(video_info.id, frame_indexes, save_paths)
