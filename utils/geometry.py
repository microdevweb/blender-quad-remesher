class GeometryUtilities:
    @staticmethod
    def mesh_bounds(vertices):
        """Calculate the bounding box of a mesh given its vertices."""
        min_x = min(vertices, key=lambda v: v[0])[0]
        max_x = max(vertices, key=lambda v: v[0])[0]
        min_y = min(vertices, key=lambda v: v[1])[1]
        max_y = max(vertices, key=lambda v: v[1])[1]
        min_z = min(vertices, key=lambda v: v[2])[2]
        max_z = max(vertices, key=lambda v: v[2])[2]
        return (min_x, min_y, min_z), (max_x, max_y, max_z)

    @staticmethod
    def vertex_normals(vertices, faces):
        """Calculate the normals for each vertex based on the faces they belong to."""
        from collections import defaultdict
        import numpy as np

        normals = defaultdict(np.array)
        count = defaultdict(int)

        for face in faces:
            v0, v1, v2 = [vertices[i] for i in face]
            edge1 = np.array(v1) - np.array(v0)
            edge2 = np.array(v2) - np.array(v0)
            normal = np.cross(edge1, edge2)
            normal /= np.linalg.norm(normal)

            for vertex in face:
                normals[vertex] += normal
                count[vertex] += 1

        return {v: (normals[v] / count[v]).tolist() for v in normals}

    @staticmethod
    def edge_length(v1, v2):
        """Calculate the length of an edge given two vertices."""
        import numpy as np
        return np.linalg.norm(np.array(v2) - np.array(v1))

    @staticmethod
    def face_area(v1, v2, v3):
        """Calculate the area of a triangle given its vertices."""
        import numpy as np
        edge1 = np.array(v2) - np.array(v1)
        edge2 = np.array(v3) - np.array(v1)
        return np.linalg.norm(np.cross(edge1, edge2)) / 2.0

