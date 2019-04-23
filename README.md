# vertexgrouptools

Filter vertices based on the number of vertex groups they're on. For blender 2.8.

# But why?

Certain game engines limit the total number of influencers per vertex. For example, babylon.js only allows 4 influencers per vertex. With this addon you can easily see which vertices have more than X influencers.

# How does it work?

You can run this as a script, or install it as an addon. In Edit Mode, open up the n-panel. There should be a tab on the n-panel that says "Vertex Group Tools". Select the minimum number of vertex groups you want a vertex to be in (with "vg_num"). Then press "Filter Vertices". The selected vertices will be in at least "vg_num" vertex groups.

"Find Vertex Groups" shows the name of the vertex groups for all the selected vertices. If you go to the "View" tab on the n-panel and click on a single vertex, blender will also show you all the vertex groups for the selected vertex. (note, this blender feature only works if a single vertex is selected. The "Find Vertex Groups" feature of this addon works if multiple vertices are selected). 

# Hope it helps!