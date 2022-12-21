import os
from shutil import rmtree

from dotenv import load_dotenv
import supervisely as sly
from supervisely.project.project_type import ProjectType

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

workspace_id = sly.env.workspace_id()

original_dir = "src/videos/original"
result_dir = "src/videos/result"

# Remove the results directory if it exists.
if os.path.exists(result_dir):
    rmtree(result_dir)
os.mkdir(result_dir)

# Create a new Supervisely project.
project = api.project.create(
    workspace_id, "Animals", type=ProjectType.VIDEOS, change_name_if_conflict=True
)

# Create a new Supervisely dataset.
dataset = api.dataset.create(project.id, "Birds")


# Upload the video from the local directory to the Supervisely platform.
path = os.path.join(original_dir, "Penguins.mp4")
meta = {"my-field-1": "my-value-1", "my-field-2": "my-value-2"}

video = api.video.upload_path(
    dataset.id,
    name="Penguins",
    path=path,
    meta=meta,  # optional: you can add metadata to the video.
)
print(f'✅ Video "{video.name}" uploaded to the Supervisely platform with ID:{video.id}')

# Get information about the video from Supervisely by id.
video_info = api.video.get_info_by_id(video.id)
print(f"✅ Video id - {video_info.id}")

# Get information about the video from Supervisely by name and dataset ID.
video_info_by_name = api.video.get_info_by_name(dataset.id, video.name)
print(f"✅ Video name - {video_info_by_name.id}")


# Upload a list of videos from the local directory to the Supervisely platform.
names = ["Flamingo.mp4", "Swans.mp4", "Toucan.mp4"]
paths = [os.path.join(original_dir, name) for name in names]

# This method uses fewer requests to the database and allows to upload more videos efficiently.
upload_info = api.video.upload_paths(dataset.id, names, paths)
print(f"✅ {len(upload_info)} videos successfully uploaded to the Supervisely platform")


# Get a list of all the videos from the Supervisely dataset.
video_info_list = api.video.get_list(dataset.id)
print(f"✅ {len(video_info_list)} videos information received.")


# Download the video from the Supervisely platform to the local directory by id.
save_path = os.path.join(result_dir, f"{video_info.name}.mp4")
api.video.download_path(video_info.id, save_path)
print(f"✅ Video has been successfully downloaded to '{save_path}'")


# Download the frame of the video as an image from the Supervisely platform to the local directory.
frame_idx = 15
file_name = "frame.png"
save_path = os.path.join(result_dir, file_name)
api.video.frame.download_path(video_info.id, frame_idx, save_path)
print(f"✅ Video frame has been successfully downloaded as an image to '{save_path}'")


# You can also download the video frame in RGB NumPy matrix format.
video_frame_np = api.video.frame.download_np(video_info.id, frame_idx)
print(f"✅ Video frame downloaded in RGB NumPy matrix. Frame shape: {video_frame_np.shape}")


# Download the range of video frames as images from the Supervisely platform to the local directory
frame_indexes = [5, 10, 20, 30, 45]
save_paths = [os.path.join(result_dir, f"frame_{idx}.png") for idx in frame_indexes]

# This method uses fewer requests to the database and downloads more videos efficiently.
api.video.frame.download_paths(video_info.id, frame_indexes, save_paths)
print(f"✅ {len(frame_indexes)} images has been successfully downloaded to '{save_path}'")


# Download the range of video frames in RGB NumPy matrix format from the Supervisely platform.
video_frames_np = api.video.frame.download_nps(video_info.id, frame_indexes)
print(f"✅ {len(video_frames_np)} video frames downloaded in RGB NumPy matrix.")
