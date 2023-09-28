from magicgui import magicgui
import napari
from napari import Viewer
from napari.layers import Image, Points
import cv2
import numpy as np
from napari.qt.threading import thread_worker



def normalize_stack(stack, **kwargs):
    '''
    -normalizes n-dimensional stack it to its maximum and minimum values,
    unless normalization values are provided in kwargs,
    -casts the image to 8 bit for fast processing with cv2
    '''
    img = np.float32(stack)
    if 'vmin' in kwargs:
        vmin = kwargs['vmin']
    else:    
        vmin = np.amin(img)
   
    if 'vmax' in kwargs:
        vmax = kwargs['vmax']
    else:    
        vmax = np.amax(img)
    saturation = 1   
    img = saturation * (img-vmin) / (vmax-vmin)
    img = (img*255).astype('uint8') 
    return img, vmin, vmax

def filter_image(img, sigma):
    if sigma >0:
        sigma = (sigma//2)*2+1 # sigma must be odd in cv2  
        filtered = cv2.medianBlur(img,sigma)
        return filtered
    else:
        return img
    
def select_rois(image, positions, roi_size):
    
    rois = []
    half_size = roi_size//2
    for pos in positions:
        y = int(pos[0])
        x = int(pos[1])
        rois.append(image[y-half_size:y+half_size,
                                x-half_size:x+half_size])
    return rois
            
def align_with_registration(next_rois, previous_rois, filter_size, roi_size):  
    
    original_rois = []
    aligned_rois = []
    dx_list = []
    dy_list = []
    
    half_size = roi_size//2
    
    warp_mode = cv2.MOTION_TRANSLATION 
    number_of_iterations = 5000
    termination_eps = 1e-10
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                    number_of_iterations,  termination_eps)
    
    for previous_roi, next_roi in zip(previous_rois, next_rois):
      
        previous_roi = filter_image(previous_roi, filter_size)
        next_roi = filter_image(next_roi, filter_size)
        
        sx,sy = previous_roi.shape
        
        warp_matrix = np.eye(2, 3, dtype=np.float32)
        
        try:
            _, warp_matrix = cv2.findTransformECC (previous_roi, next_roi,
                                                      warp_matrix, warp_mode, criteria)
            
            next_roi_aligned = cv2.warpAffine(next_roi, warp_matrix, (sx,sy),
                                           flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        except:
            next_roi_aligned = next_roi
        
        original_roi = previous_roi[sy//2-half_size:sy//2+half_size,
                                        sx//2-half_size:sx//2+half_size ]
        
        aligned_roi =  next_roi_aligned[sy//2-half_size:sy//2+half_size,
                                        sx//2-half_size:sx//2+half_size ]
    
        original_rois.append(original_roi)
        aligned_rois.append(aligned_roi)
        
        dx = warp_matrix[0,2]
        dy = warp_matrix[1,2]
        
        dx_list.append(dx)
        dy_list.append(dy)
    
    return aligned_rois, original_rois, dx_list, dy_list

def update_position(old_positions, dx_list, dy_list ):
    
    next_positions = []
    roi_idx = 0
    for pos, dx, dy in zip(old_positions, dx_list, dy_list):
        y1 = pos[0] + dy
        x1 = pos[1] + dx
        next_positions.append([y1,x1])  
        roi_idx +=1
        
    return next_positions

def zoom_stack(aligned, roi_size, zoom):

    st, sr, sy, sx = aligned.shape
    zoomed = np.zeros((st,sr,sy*zoom, sx*zoom))
    for t_idx in range (st):
        for roi_idx in range (sr):
            zoomed[t_idx, roi_idx, :,:] = cv2.resize(aligned[t_idx, roi_idx,:,:], [zoom*roi_size,zoom*roi_size])
    return zoomed

@magicgui(call_button="Register ROIs")
def register_ROIs(viewer: Viewer,
              image: Image,
              points_layer: Points,
              roi_size:int = 100,
              zoom: int = 4,
              median_filter_size:int = 3
              ):
            
    original_stack = np.asarray(image.data)
    st,sy,sx = original_stack.shape
    normalized, vmin, vmax = normalize_stack(original_stack)
    points = np.asarray(points_layer.data)
    initial_yx_coordinates = points[:,[1,2]]
    positions_list = initial_yx_coordinates
    aligned_images = []
    filtered_starting_rois = []

    previous_rois = select_rois(normalized[0,:,:],initial_yx_coordinates,roi_size)
    for roi in previous_rois:
        filtered_roi = filter_image(roi, median_filter_size)
        filtered_starting_rois.append(filtered_roi)
    roi_num = len(previous_rois)
    aligned_images.append(filtered_starting_rois)
            
    next_rois = select_rois(normalized[1,:,:],positions_list,roi_size)
    aligned, original, dx, dy = align_with_registration(next_rois,
                                                        previous_rois,
                                                        median_filter_size,
                                                        roi_size)
    
    aligned_images.append(aligned)
    positions_list = update_position(positions_list, dx, dy)
    aligned_array = np.array(aligned_images)
    zoomed_array = zoom_stack(aligned_array, roi_size, zoom)
    for roi_idx in range (roi_num):
        #viewer.add_image(aligned_array[:,roi_idx,:,:], name = f'aligned_roi{roi_idx}')
        viewer.add_image(zoomed_array[:,roi_idx,:,:], name = f'aligned_roi{roi_idx}')
if __name__ == '__main__':
    
    viewer = Viewer()
    # register_ROIs_widget = register_ROIs()
    viewer.window.add_dock_widget(register_ROIs, name = 'Register ROIs',
                                  area='right', add_vertical_stretch=True)
    napari.run()