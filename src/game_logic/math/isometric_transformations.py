from game_data.camera.movement_bounds import CameraMovementBounds
from game_data.camera.transform import CameraTransform
from game_data.game_context.world.map.map_metadata import MapMetaData
from game_data.physics.rectangle import Rectangle
from game_data.rendering.viewport.viewport import ViewPort
from game_data.rendering.viewport.viewport_dimensions import ViewportDimensions


def isometricTransform(pos):
    x, y = pos
    return (x-y, .5*(x+y))

def get_transformed_rectangle_for_cam_scaling_focus_on_screen_center(rectangle: Rectangle, viewport_dimensions: ViewportDimensions, camera_transform: CameraTransform) -> Rectangle:
    pcam_x = camera_transform.x
    pcam_y = camera_transform.y
    scale = camera_transform.s
    x = rectangle.x
    y = rectangle.y
    width = rectangle.w
    height = rectangle.h
    screen_width = viewport_dimensions.pixel_width
    screen_height = viewport_dimensions.pixel_height
    return Rectangle(scale*x+(screen_width/2)*(scale+1)-scale*pcam_x, scale*y+(screen_height/2)*(scale+1)-scale*pcam_y, width*scale, height*scale)

def rect_in_screen_bounds(viewport_dimensions: ViewportDimensions, rectangle: Rectangle) -> bool:
        x1 = rectangle.x
        y1 = rectangle.y
        x2 = x1+rectangle.w
        y2 = y1+rectangle.h
        return not (y2 <= 0 or y1 >= viewport_dimensions.pixel_height or x2 <= 0 or x1 >= viewport_dimensions.pixel_width) 

def update_cam_restriction_box(map_metadata: MapMetaData, camera_transform: CameraTransform, bounding_box_to_update: CameraMovementBounds, viewport_dimensions: ViewportDimensions):
    cam_x, cam_y = camera_transform.x, camera_transform.y
    camera_transform.x = 0
    camera_transform.y = 0

    map_width = map_metadata.width
    map_height = map_metadata.height
    tileSize = map_metadata.tile_size

    bounding_box_to_update.left = get_transformed_isometric_screen_position_from_tile_position(map_width-1, 0, map_metadata=map_metadata, viewport_dimensions=viewport_dimensions, camera_transform=camera_transform)[0]
    bounding_box_to_update.bottom = get_transformed_isometric_screen_position_from_tile_position(map_width-1, map_height-1, map_metadata=map_metadata, viewport_dimensions=viewport_dimensions, camera_transform=camera_transform)[1]

    bounding_box_to_update.right = get_transformed_isometric_screen_position_from_tile_position(0, map_height-1, map_metadata=map_metadata, viewport_dimensions=viewport_dimensions, camera_transform=camera_transform)[0]
    bounding_box_to_update.up = get_transformed_isometric_screen_position_from_tile_position(0, 0, map_metadata=map_metadata, viewport_dimensions=viewport_dimensions, camera_transform=camera_transform)[1]

    camera_transform.x = cam_x
    camera_transform.y = cam_y

def isometric_tile_in_viewport(t_x, t_y, map_meta_data: MapMetaData, viewport: ViewPort) -> bool:
    tileSize = map_meta_data.tile_size
    cam_s = viewport.camera_transform.s
    dx, dy = get_transformed_isometric_screen_position_from_tile_position(t_x, t_y, map_metadata=map_meta_data, viewport_dimensions=viewport.dimensions, camera_transform=viewport.camera_transform)
    rect = Rectangle(dx-tileSize*cam_s, dy, tileSize*2*cam_s, tileSize*cam_s)
    return rect_in_screen_bounds(rect)

def position_in_screen_bounds(world_x, world_y, viewport_dimensions: ViewportDimensions) -> bool:
    screen_width = viewport_dimensions.pixel_width
    screen_height = viewport_dimensions.pixel_height
    tx, ty = get_transformed_isometric_screen_position(world_x, world_y)
    return 0 <= tx <= screen_width and 0 <= ty <= screen_height

def get_transformed_isometric_world_position(pixel_x, pixel_y, viewport_dimensions: ViewportDimensions, camera_transform: CameraTransform):
        cam_s = camera_transform.s
        cam_x = camera_transform.x
        cam_y = camera_transform.y
        
        screen_width = viewport_dimensions.pixel_width
        screen_height = viewport_dimensions.pixel_height

        tx = (screen_width/2)*(cam_s+1)-cam_s*cam_x
        ty = (screen_height/2)*(cam_s+1)-cam_s*cam_y
        m = (pixel_x-tx)/cam_s
        w = 2*(pixel_y-ty)/cam_s
        rx = (m+w)/2
        return (rx, w-rx)

def get_transformed_isometric_screen_position_from_tile_position(tile_x, tile_y, map_metadata: MapMetaData, viewport_dimensions: ViewportDimensions, camera_transform: CameraTransform):
    return get_transformed_isometric_screen_position(tile_x*map_metadata.tile_size, tile_y*map_metadata.tile_size, viewport_dimensions=viewport_dimensions, camera_transform=camera_transform)

def get_transformed_isometric_screen_position(world_x, world_y, viewport_dimensions: ViewportDimensions, camera_transform: CameraTransform):
    cam_s = camera_transform.s
    cam_x = camera_transform.x
    cam_y = camera_transform.y

    screen_width = viewport_dimensions.pixel_width
    screen_height = viewport_dimensions.pixel_height

    return (cam_s*(world_x-world_y)+(screen_width/2)*(cam_s+1)-cam_s*cam_x,(cam_s/2)*(world_x+world_y)+(screen_height/2)*(cam_s+1)-cam_s*cam_y)

def get_transformed_scaled_position(x, y, camera_transform: CameraTransform, viewport_dimensions: ViewportDimensions):
    rect = get_transformed_rectangle_for_cam_scaling_focus_on_screen_center(rectangle=Rectangle(x, y, 1, 1), viewport_dimensions=viewport_dimensions, camera_transform=camera_transform)
    return (rect.x, rect.y, rect.w)

def get_transformed_rect_position(rectangle: Rectangle, viewport_dimensions: ViewportDimensions, camera_transform: CameraTransform):
    return get_transformed_rectangle_for_cam_scaling_focus_on_screen_center(rectangle=rectangle, viewport_dimensions=viewport_dimensions, camera_transform=camera_transform)

def get_transformed_position(x, y, viewport_dimensions: ViewportDimensions, camera_transform: CameraTransform):
    rect = get_transformed_rectangle_for_cam_scaling_focus_on_screen_center(rectangle=Rectangle(x, y, 0, 0), viewport_dimensions=viewport_dimensions, camera_transform=camera_transform)
    return (rect.x, rect.y)
