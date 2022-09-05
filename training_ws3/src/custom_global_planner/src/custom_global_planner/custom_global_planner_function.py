#!/usr/bin/env python3

def make_trajectory(x1, y1, ori1,
                    x2, y2, ori2,
                    costmap, costmap_resolution,
                    costmap_origin_x, costmap_origin_y):
    print('Python called! costmap size is {} x {}'.format(
        len(costmap), len(costmap[0])))
    return (True, [(x1, y1, ori1),
                   # TODO improve orientation processing
                   ((x1+x2)*0.5, (y1+y2)*0.5, (ori1+ori2)*0.5), 
                   (x2, y2, ori2)])
