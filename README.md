# DiamondSquare
This is a Python 3.7 implementation of a diamond-square algorithm, used for procedural heightmap/terrain generation.
## 1. Usage
The script can be run directly, or from the command line. By default it will output a 513x513 image file to its folder, as well as displaying a 2D heightmap in Matplotlib and a 3D visualization of that heightmap using Mayavi. When run via the command line, several arguments can be passed:
>**Any integer**: If provided, this must be the first argument given. This determines the height and width of the heightmap, which defaults to 513x513 otherwise. *For the algorithm to work properly, this integer must be 2^n + 1 (3, 5, 9, 17, etc.)!* Feel free to experiment with other values, though, to get some interesting results.<br><br>
**-ns**: The program will not output an image file.<br><br>
**-2donly**: The program will only display a 2D Matplotlib heightmap.<br><br>
**-3donly**: The program will only display a 3D Mayavi heightmap.<br><br>
**-x**: The program will display neither a 2D nor 3D heightmap. Has the same effect as passing both *-2donly* and *-3donly* arguments.

Obviously, the larger the array, the higher the computation time. For every power of 2, the time will increase by roughly four times. On my machine, a 257x257 array takes about 1 second, a 513x513 array takes 4, and a 1025x1025 array takes 18.
## 2. Example Results
TBA
