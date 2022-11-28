<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h2 align="center">Descriptools for QGIS</h2>
  <p align="center">
    A QGIS plug-in for terrain descriptor calculation/delineation.
    <br />
    ·
    <a href="https://github.com/JVBSouza/descriptools-for-qgis/issues">Report Bug</a>
    ·
    <a href="https://github.com/JVBSouza/descriptools-for-qgis/issues">Request Feature</a>
  </p>
</p>
<br />



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
Terrain descriptors are different data extracted from earth's surface and topography </br>
This information may be used in different fields, including natural disaster management, such as floods or earth slides. </br>
This toolbox provides the calculation of 8 terrain descriptors, through the use of methods available in the [Descriptools toolbox](https://github.com/JVBSouza/descriptools) 

### Built With

* [Python](https://www.python.org/)
* [Descriptools](https://github.com/JVBSouza/descriptools)


<!-- GETTING STARTED -->
## Getting Started
To get the plug-in running on QGIS, follow these steps:

1. Download the repository as .zip file
2. In QGIS, select "Manage and Install Plugins" then "Install from ZIP"
3. There, select the downloaded .zip file and click "Install Plugin". "A warning should pop about missing modules"
4. The descritools package is required. To install it, open the QGIS OSGeo4W shell and install it with pip.

<br/>

### Installing Descriptools
You can install Descriptools using pip, following these steps:
   1. Go to programs files where QGIS is installed (E.g. C:\Program Files\QGIS 3.24.2)
   2. Open OSGeo4W .bat file
   3. In the command line, run:
      ```sh
      pip install descriptools
      ```


<!-- LICENSE -->
## License

Distributed under the GNU License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Authors: José Vinícius Boing de Souza and Fabiane Dorneles

Contact address: joseboing@gmail.com and fabiane.mail.d@gmail.com

Project Link: [https://github.com/JVBSouza/descriptools-for-qgis](https://github.com/JVBSouza/descriptools-for-qgis)