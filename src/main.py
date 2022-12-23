import os
from shutil import rmtree

from dotenv import load_dotenv
from pprint import pprint
import supervisely as sly
from supervisely.project.project_type import ProjectType

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

workspace_id = sly.env.workspace_id()

original_dir = "src/videos/original"
result_dir = "src/videos/result"

# Remove results directory if it exists.
if os.path.exists(result_dir):
    rmtree(result_dir)
os.mkdir(result_dir)

# Create new Supervisely project.
project = api.project.create(
    workspace_id, "Animals", type=ProjectType.VIDEOS, change_name_if_conflict=True
)
print(f"Project ID: {project.id}")

# Create new Supervisely dataset.
dataset = api.dataset.create(project.id, "Birds")
print(f"Dataset ID: {dataset.id}")

# Upload video from local directory to Supervisely platform.
path = os.path.join(original_dir, "Penguins.mp4")

video = api.video.upload_path(
    dataset.id,
    name="Penguins",
    path=path,
)
print(f'Video "{video.name}" uploaded to Supervisely platform with ID:{video.id}')


# Upload list of videos from local directory to Supervisely platform.
names = ["Flamingo.mp4", "Swans.mp4", "Toucan.mp4"]
paths = [os.path.join(original_dir, name) for name in names]

# This method uses fewer requests to database and allows to upload more videos efficiently.
upload_info = api.video.upload_paths(dataset.id, names, paths)
print(f"{len(upload_info)} videos successfully uploaded to Supervisely platform")


# Get information about video from Supervisely by id.
video_info = api.video.get_info_by_id(video.id)
print(video_info)

# Get information about video from Supervisely by name and dataset ID.
video_info_by_name = api.video.get_info_by_name(dataset.id, video.name)
print(f"Video name - {video_info_by_name.name}")

# Get list of all videos from Supervisely dataset.
video_info_list = api.video.get_list(dataset.id)
print(f"{len(video_info_list)} videos information received.")


# Download video from Supervisely platform to local directory by id.
save_path = os.path.join(result_dir, f"{video_info.name}.mp4")
api.video.download_path(video_info.id, save_path)
print(f"Video has been successfully downloaded to '{save_path}'")


# Get video metadata from file
video_path = "src/videos/result/Penguins.mp4"
file_info = sly.video.get_info(save_path)
pprint(file_info)


# Get video metadata from server
api.video.get_info_by_id
video_info = api.video.get_info_by_id(video.id)
print(video_info.file_meta)

# Download frame of video from Supervisely platform as image and save to local directory.
frame_idx = 15
file_name = "frame.png"
save_path = os.path.join(result_dir, file_name)
api.video.frame.download_path(video_info.id, frame_idx, save_path)
print(f"Video frame has been successfully downloaded as an image to '{save_path}'")


# You can also download video frame as RGB NumPy matrix.
video_frame_np = api.video.frame.download_np(video_info.id, frame_idx)
print(f"Video frame downloaded in RGB NumPy matrix. Frame shape: {video_frame_np.shape}")


# Download multiple frames from Supervisely platform as images and save to local directory
frame_indexes = [5, 10, 20, 30, 45]
save_paths = [os.path.join(result_dir, f"frame_{idx}.png") for idx in frame_indexes]

# This method uses fewer requests to database and downloads more videos efficiently.
api.video.frame.download_paths(video_info.id, frame_indexes, save_paths)
print(f"{len(frame_indexes)} images has been successfully downloaded to '{save_path}'")


# Download range of video frames as RGB NumPy matrix from Supervisely platform.
video_frames_np = api.video.frame.download_nps(video_info.id, frame_indexes)
print(f"{len(video_frames_np)} video frames downloaded in RGB NumPy matrix.")

# Remove video from Supervisely platform by id
api.video.remove(video_info.id)
print(f"Video (ID: {video_info.id}) successfully removed")


# Remove list of videos from Supervisely platform by ids
videos_to_remove = api.video.get_list(dataset.id)
remove_ids = [video.id for video in videos_to_remove]
api.video.remove_batch(remove_ids)
print(f"{len(remove_ids)} videos successfully removed.")
