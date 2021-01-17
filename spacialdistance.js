function spatialDistance(x1,y1,x2,y2,xmax,ymax,height,angle,fov) {
    //Enter x and y as pixel positions of the feet (center is 0,0)
    //xmax is maximum x coord, ymax is maximum y coord (half resolution)
    //fov is horizontal fov in radians, angle is radians below horizontal (positive)
    //Returns the distance between (x1,y1) and (x2,y2) in 3D space based on
    const yfov = 2 * Math.atan((ymax/xmax)*Math.tan(fov/2));
    const a1 = height * Math.tan(0.5*Math.PI-angle+vfov/2*(y1/ymax)); //a refers to the forward dimension
    const a2 = height * Math.tan(0.5*Math.PI-angle+vfov/2*(y2/ymax));
    const b1 = a1 * Math.tan(fov/2*(x1/xmax)); //b refers to perpendicular dimension
    const b2 = a2 * Math.tan(fov/2*(x2/xmax));
    return ((a2-a1)**2+(b2-b1)**2)**0.5;
}