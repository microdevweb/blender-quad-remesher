"""
Quad Remeshing Algorithms

This module contains the core algorithms for converting meshes to quad topology.
Includes adaptive remeshing, uniform remeshing, and optimization techniques.
"""

import bmesh
import numpy as np
from mathutils import Vector


def adaptive_remesh(bm, density=1.0, iterations=5):
    """
    Adaptive remeshing algorithm that adjusts mesh density based on curvature.
    
    Args:
        bm: BMesh object to remesh
        density: Global density multiplier (1.0 = default)
        iterations: Number of refinement iterations
    
    Returns:
        bool: Success status
    """
    try:
        # Analyze mesh curvature
        curvatures = calculate_vertex_curvature(bm)
        
        # Subdivide high-curvature areas
        edges_to_subdivide = []
        for edge in bm.edges:
            v1, v2 = edge.verts
            avg_curvature = (curvatures.get(v1.index, 0) + curvatures.get(v2.index, 0)) / 2
            
            # Subdivide if curvature is high
            if avg_curvature > 0.5 / density:
                edges_to_subdivide.append(edge)
        
        # Perform subdivision
        if edges_to_subdivide:
            bmesh.ops.subdivide_edges(bm, edges=edges_to_subdivide, number_cuts=1)
        
        # Smooth vertices
        for _ in range(iterations):
            smooth_mesh(bm, factor=0.3)
        
        return True
    except Exception as e:
        print(f"Error in adaptive_remesh: {e}")
        return False


def uniform_remesh(bm, target_edge_length=1.0):
    """
    Create uniform quad remesh with consistent edge length.
    
    Args:
        bm: BMesh object
        target_edge_length: Desired edge length
    
    Returns:
        bool: Success status
    """
    try:
        # Subdivide edges that are too long
        edges_to_split = []
        for edge in bm.edges:
            length = get_edge_length(edge)
            if length > target_edge_length * 1.5:
                edges_to_split.append(edge)
        
        if edges_to_split:
            bmesh.ops.subdivide_edges(bm, edges=edges_to_split, number_cuts=1)
        
        # Collapse edges that are too short
        edges_to_collapse = []
        for edge in bm.edges:
            length = get_edge_length(edge)
            if length < target_edge_length * 0.5 and len(edge.link_faces) == 2:
                edges_to_collapse.append(edge)
        
        # Carefully collapse edges
        for edge in edges_to_collapse:
            try:
                bmesh.ops.collapse_short_edges(bm, edges=[edge])
            except:
                pass
        
        return True
    except Exception as e:
        print(f"Error in uniform_remesh: {e}")
        return False


def optimize_remesh(bm, density=1.0):
    """
    Optimize topology for animation and deformation.
    
    Args:
        bm: BMesh object
        density: Mesh density
    
    Returns:
        bool: Success status
    """
    try:
        # First apply adaptive remesh
        adaptive_remesh(bm, density)
        
        # Optimize for animation - reduce extraordinary vertices
        for _ in range(3):
            optimize_topology(bm)
        
        return True
    except Exception as e:
        print(f"Error in optimize_remesh: {e}")
        return False


def smooth_mesh(bm, iterations=1, factor=0.5):
    """
    Apply Laplacian smoothing to mesh.
    
    Args:
        bm: BMesh object
        iterations: Number of smoothing iterations
        factor: Smoothing strength (0.0-1.0)
    """
    for _ in range(iterations):
        for vert in bm.verts:
            if not vert.hide and len(vert.link_edges) > 0:
                # Calculate average position of neighbors
                neighbors = []
                for edge in vert.link_edges:
                    neighbor = edge.other_vert(vert)
                    if not neighbor.hide:
                        neighbors.append(neighbor.co)
                
                if neighbors:
                    avg_pos = sum(neighbors, Vector()) / len(neighbors)
                    vert.co = vert.co.lerp(avg_pos, factor)


def convert_to_quads(bm):
    """
    Convert mesh triangles to quads where possible.
    
    Args:
        bm: BMesh object
    
    Returns:
        int: Number of faces merged
    """
    merged = 0
    
    try:
        # Get all triangles
        triangles = [f for f in bm.faces if len(f.verts) == 3]
        processed = set()
        
        for tri in triangles:
            if tri.index in processed:
                continue
            
            # Try to find adjacent triangle to merge
            for edge in tri.edges:
                if len(edge.link_faces) == 2:
                    other_face = None
                    for face in edge.link_faces:
                        if face.index != tri.index:
                            other_face = face
                            break
                    
                    if other_face and other_face.index not in processed:
                        if len(other_face.verts) == 3:
                            try:
                                bmesh.ops.join_faces(bm, faces=[tri, other_face])
                                processed.add(tri.index)
                                processed.add(other_face.index)
                                merged += 1
                                break
                            except:
                                pass
    except Exception as e:
        print(f"Error in convert_to_quads: {e}")
    
    return merged


def calculate_vertex_curvature(bm):
    """
    Calculate mean curvature for each vertex.
    
    Args:
        bm: BMesh object
    
    Returns:
        dict: Vertex index -> curvature value
    """
    curvatures = {}
    
    try:
        for vert in bm.verts:
            if len(vert.link_edges) < 2:
                curvatures[vert.index] = 0
                continue
            
            # Calculate mean curvature using dihedral angles
            angle_sum = 0
            for edge in vert.link_edges:
                if len(edge.link_faces) == 2:
                    f1, f2 = edge.link_faces
                    angle = f1.normal.angle(f2.normal)
                    angle_sum += angle
            
            curvatures[vert.index] = angle_sum / len(vert.link_edges)
    except Exception as e:
        print(f"Error calculating curvature: {e}")
    
    return curvatures


def optimize_topology(bm):
    """
    Optimize mesh topology by fixing extraordinary vertices.
    
    Args:
        bm: BMesh object
    """
    try:
        # Find extraordinary vertices (valence != 4)
        extraordinary_verts = [v for v in bm.verts if len(v.link_edges) != 4]
        
        # Apply slight smoothing to reduce distortion
        for vert in extraordinary_verts:
            if not vert.hide and len(vert.link_edges) > 0:
                neighbors = [edge.other_vert(vert).co for edge in vert.link_edges]
                if neighbors:
                    avg_pos = sum(neighbors, Vector()) / len(neighbors)
                    vert.co = vert.co.lerp(avg_pos, 0.1)
    except Exception as e:
        print(f"Error in optimize_topology: {e}")


def get_edge_length(edge):
    """
    Calculate the length of an edge.
    
    Args:
        edge: BMesh edge
    
    Returns:
        float: Edge length
    """
    v1, v2 = edge.verts
    return (v1.co - v2.co).length


def get_face_area(face):
    """
    Calculate the area of a face.
    
    Args:
        face: BMesh face
    
    Returns:
        float: Face area
    """
    if len(face.verts) < 3:
        return 0
    
    # Use triangulation for accurate area
    verts = face.verts
    area = 0
    
    for i in range(1, len(verts) - 1):
        v1 = verts[0].co
        v2 = verts[i].co
        v3 = verts[i + 1].co
        area += ((v2 - v1).cross(v3 - v1)).length / 2
    
    return area


def apply_density_map(bm, density_map):
    """
    Apply per-vertex density values from a vertex group.
    
    Args:
        bm: BMesh object
        density_map: Dict of vertex index -> density value
    """
    try:
        for vert in bm.verts:
            density = density_map.get(vert.index, 1.0)
            # Store in vertex for later use
            vert.tag = density
    except Exception as e:
        print(f"Error applying density map: {e}")


def decimate_mesh(bm, ratio=0.5):
    """
    Decimate mesh to reduce polygon count.
    
    Args:
        bm: BMesh object
        ratio: Target ratio (0.0-1.0)
    
    Returns:
        bool: Success status
    """
    try:
        bmesh.ops.decimate(bm, ratio=ratio)
        return True
    except Exception as e:
        print(f"Error in decimate_mesh: {e}")
        return False


def subdivide_smooth(bm, iterations=1):
    """
    Apply Catmull-Clark subdivision.
    
    Args:
        bm: BMesh object
        iterations: Number of subdivision levels
    
    Returns:
        bool: Success status
    """
    try:
        for _ in range(iterations):
            bmesh.ops.subdivide_smooth(
                bm,
                number_cuts=1,
                smoothness=1.0,
                quad_corner_type='STRAIGHT_CUT'
            )
        return True
    except Exception as e:
        print(f"Error in subdivide_smooth: {e}")
        return False


def remesh_quad(obj, density=1.0, use_smooth=True):
    """
    Main function to remesh an object with quad topology.
    
    Args:
        obj: Blender object to remesh
        density: Remesh density (1.0 = default)
        use_smooth: Apply smoothing after remesh
    
    Returns:
        bool: Success status
    """
    try:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        
        # Convert triangles to quads
        convert_to_quads(bm)
        
        # Apply adaptive remeshing
        adaptive_remesh(bm, density)
        
        # Optional smoothing
        if use_smooth:
            smooth_mesh(bm, iterations=2, factor=0.5)
        
        # Update mesh
        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()
        
        return True
    except Exception as e:
        print(f"Error in remesh_quad: {e}")
        return False
