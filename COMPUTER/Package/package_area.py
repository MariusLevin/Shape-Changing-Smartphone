"""
@object: Implementation area functions to concave form
@author: PECCHIOLI Mathieu
"""
# LIBRAIRIES IMPORT
from numpy import sqrt

def add_edge(edges, edge_points,i, j, pts):
     """Ajoute une ligne entre le i ème point et le j ème points si elle n'est pas dans la liste"""
     if (i, j) in edges or (j, i) in edges:
        # déjà dans la liste
        return
     edges.add( (i, j) )
     edge_points.append(pts[ [i, j] ])
 
def calc_alpha2(alpha, tri, pts):
     edges = set()
     edge_points = []
     area = 0
     # loop over triangles:
     for ia, ib, ic in tri.vertices:
         # extraction des points de Delaunay
         pa = ((2.26 * 25.4) / 320) * pts[ia]
         pb = ((2.26 * 25.4) / 320) * pts[ib]
         pc = ((2.26 * 25.4) / 320) * pts[ic]
         # Longueurs des cotés du triangle
         a = sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
         b = sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
         c = sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
         # Semiperimètre du triangle
         s = (a + b + c)/2.0
         # Surface du triangle par la formule de Heron
         areaTriangle = sqrt(s* (s-a) * (s-b) * (s-c))
         # rayon de filtrage
         circum_r = a * b * c / (4.0 * areaTriangle)
         if circum_r < alpha:
            add_edge(edges,edge_points, ia, ib, pts)
            add_edge(edges,edge_points,ib, ic, pts)
            add_edge(edges,edge_points,ic, ia, pts)
            area = area + areaTriangle
     return edge_points, area