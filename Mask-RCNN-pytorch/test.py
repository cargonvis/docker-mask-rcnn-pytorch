import os
import cv2
import argparse
import matplotlib.pyplot as plt
from mask_rcnn import segmentation_model, plot_masks
from tqdm import tqdm  # Import tqdm for the progress bar

def process_frame(frame, model, classes):
    pred = model.detect_masks(frame, rgb_image=False)
    plotted = plot_masks(frame, pred, classes)
    return plotted

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help='path to input image or video')
    parser.add_argument('--labels', type=str, default='./my_dataset/labels.txt', help='path to labels list text file (labels.txt)')
    parser.add_argument('--model', type=str, default='./maskrcnn_saved_models/mask_rcnn_model.pt', help='path to saved model')
    
    args = parser.parse_args()
    
    INPUT_PATH = args.input
    MODEL_PATH = args.model
    LABEL_PATH = args.labels
    
    with open(LABEL_PATH,'r') as f:
        lines = [line.rstrip() for line in f]
    assert lines[0] == '__ignore__', """first line of labels file must be  \
                                        "__ignore__" (labelme labels.txt)"""
    lines.pop(0) # remove first element [__ignore__]
    
    num_classes = len(lines)
    classes = dict(zip(range(num_classes),lines))
    
    model = segmentation_model(MODEL_PATH, num_classes)
    
    if os.path.isfile(INPUT_PATH):
        _, file_extension = os.path.splitext(INPUT_PATH)
        
        if file_extension.lower() in ['.jpg', '.png', '.jpeg', '.bmp']:
            image = cv2.imread(INPUT_PATH)
            processed = process_frame(image, model, classes)
            
            os.makedirs('./results', exist_ok=True)
            cv2.imwrite('./results/processed_image.jpg', processed)
            
            plt.figure(figsize=(16,12))
            plt.imshow(processed)
            plt.show()
        
        elif file_extension.lower() in ['.mp4', '.avi', '.mkv']:
            cap = cv2.VideoCapture(INPUT_PATH)
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            
            output_path = './results/output_video.mp4'
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, 30, (frame_width, frame_height))
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            with tqdm(total=total_frames, desc="Processing frames") as pbar:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    processed = process_frame(frame, model, classes)
                    out.write(processed)
                    
                    pbar.update(1)  # Update progress bar
                    
                pbar.close()  # Close progress bar
            
            cap.release()
            out.release()
            
            # Convert frames to video using FFmpeg
            os.system(f"ffmpeg -y -i {output_path} -c:v libx264 -vf fps=30 {output_path}")
            os.remove(output_path)  # Remove temporary output video
            
        else:
            print("Unsupported file format. Supported formats: .jpg, .png, .jpeg, .bmp, .mp4, .avi, .mkv")
    
    else:
        print("Input path does not exist.")