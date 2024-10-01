import numpy as np
import cv2
import gmsh
import sys

def create_dolphin_mesh(image_path, mesh_size=0.1):
    # Initialize Gmsh
    gmsh.initialize()

    # Create a new model
    gmsh.model.add("DolphinMesh")

    # Load and process the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming the largest contour is the dolphin
    dolphin_contour = max(contours, key=cv2.contourArea)

    # Create points and lines for the contour
    points = []
    for i, point in enumerate(dolphin_contour):
        x, y = point[0]
        z = 0
        point_tag = gmsh.model.geo.addPoint(x, y, z, mesh_size)
        points.append(point_tag)

    lines = []
    for i in range(len(points)):
        line_tag = gmsh.model.geo.addLine(points[i], points[(i+1) % len(points)])
        lines.append(line_tag)

    # Create a curve loop and plane surface
    curve_loop = gmsh.model.geo.addCurveLoop(lines)
    surface = gmsh.model.geo.addPlaneSurface([curve_loop])

    # Generate the mesh
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)

    # Save the mesh
    gmsh.write("dolphin_mesh.msh")

    # Launch the Gmsh GUI
    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()

    # Finalize Gmsh
    gmsh.finalize()

if __name__ == "__main__":
    # Specify the path to your dolphin image here
    image_path = "dolphin.png"
    
    create_dolphin_mesh(image_path)
    print("Mesh generated and saved as 'dolphin_mesh.msh'")