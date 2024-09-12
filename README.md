<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/sandipanpaul06/TrIdent">
    <img src="images/fau_logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">TrIdent Documentation</h3>

  <p align="center">
    A transfer learning based tool to find signatures of selective sweeps
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/sandipanpaul06/TrIdent/issues">Report Bug</a>
    ·
    <a href="https://github.com/sandipanpaul06/TrIdent/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
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
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

* Abstract: 

Natural selection leaves detectable patterns of altered spatial diversity within genomes, and identifying affected genomic regions is crucial for understanding species and population evolution. Recent approaches to uncovering adaptive footprints leverage machine learning techniques applied to raw population genomic data. Convolutional neural networks (CNNs) are particularly effective for this task due to their ability to handle large input arrays and maintain correlations among elements. However, CNNs require large training datasets and are computationally intensive to train. Shallow CNNs, while simpler and less computationally demanding than deep CNNs, may fail to capture the complex patterns associated with the many factors that influence genomic variation. Deep CNNs, on the other hand, can capture these intricate patterns, but at the cost of requiring extensive training data and computational resources. To address these challenges, transfer learning can be employed, which conditions on a CNN pre-trained on a large, diverse dataset, that is then fine-tuned on a smaller, task-specific dataset. This approach reduces the need for extensive training data and improves training efficiency while maintaining high model performance. In a transfer learning architecture, the pre-trained deep CNN acts as a feature extractor, leveraging learned representations from a larger dataset to inform the task-specific model. In this study, we develop TrIdent, which uses transfer learning to enhance the detection and characterization of adaptive genomic regions from image representations of multilocus variation. We assess the performance of TrIdent under an array of genetic, demographic, and adaptive settings, as well as unphased data and other confounding factors. Our results demonstrate that TrIdent has significantly improved detection of adaptive regions compared to some recent approaches that operate on similar data. Additionally, we explore the interpretability of the TrIdent model through class activation maps, and we retool TrIdent to infer selection parameters underlying identified adaptive candidates. Using whole-genome haplotype data from Europeans and Africans and TrIdent trained to detect selective sweeps, we were able to recapitulate well-established sweep candidates and predict novel genes associated with cancer as highly supported sweeps. These results highlight the potential of TrIdent to contribute valuable insights into adaptive processes from genomic data.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With



* [![Python][Python.org]][Python-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

Python version 3.8.5 or above is necessary to use this software. Run the following commands to ensure you have the required version.
* check python3 version
  ```sh
  python --version
  ```

### Installation

Required python packages: pandas, tensorflow, numpy, opencv-python, scikit-learn, matplotlib

1. Clone the repo
   ```sh
   git clone https://github.com/sandipanpaul06/TrIdent.git
   ```
3. Package installation
   ```sh
   pip install pandas tensorflow numpy opencv-python-headless scikit-learn matplotlib
   ```
4. For the packages already installed, upgrade the packages to the most updated version. For example
   ```js
   pip install --upgrade tensorflow
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Data preprocessing and model training:

* 1.1. Go to TrIdent software directory. Example:
   ```sh
   cd TrIdent
   ```

* 1.2. .ms output fles:

* 1.2.1. The .ms files are located in "Datasets" folder in the TrIdent software directory. For example: */Users/user/Desktop/TrIdent/Datasets*
  
* 1.2.2. The "Datasets" folder has two example sub-folders: "Neutral" and "Sweep". The toy neutral .ms files are in the "Neutral" folder (*/Users/user/Desktop/TrIdent/Datasets/Neutral*), and the sweep .ms files are in the "Sweep" folder (*/Users/user/Desktop/TrIdent/Datasets/Sweep*).

* 1.2.3. The sweep .ms files have a prefix "Sweep", and the neutral .ms files have a prefix "Neut", followed by consecutive numbers from 1 to 100. Example: (*Sweep_1.ms, Sweep_2.ms ... Sweep_20.ms*) (*Neut_1.ms, Neut_2.ms ... Neut_20.ms*)

* 1.3. Mode: **image_generation_ms** to generate input image dataset:

* 1.3.1. Command to view the necessary arguments, run:
   ```sh
   python TrIdent.py image_generation_ms -h
   ```
* 1.3.2. Arguments: pref: .ms file prefix, outFile: Output filename, nHap: number of haplotypes, subFolder: Name of the subfolder (that contains the simulations), n: Number of .ms files of the chosen class, start: Start number of .ms files, imgDim: Image dimension. For 299 x 299, put 299

* 1.3.3. Example run with sample .ms files:

   ```sh
   python TrIdent.py -mode image_generation_ms -pref Neut -outFile neutfile -nHap 198 -subFolder Neutral -n 10 -start 1 -imgDim 299
   ```
   ```sh
   python TrIdent.py -mode image_generation_ms -pref Sweep -outFile sweepfile -nHap 198 -subFolder Sweep -n 10 -start 1 -imgDim 299
   ```

* 1.3.4. Output file will be saved in "Image_datasets" folder and output message will print which ms files passed and 'fail'ed the qualification criteria


* 1.4. Mode: **train** to train and test the binary classifier:


* 1.4.1. To view the necessary arguments, run:
   ```sh
   python TrIdent.py train -h
   ```

* 1.4.2. Arguments: Sw: Sweep filename, Ne: Neutral filename, split: Train/test split, modelName: Name of model

* 1.4.3. Example run with sample image dataset file:

   ```sh
   python TrIdent.py -mode train -Sw sweepfile -Ne neutfile -split 0.5 -modelName expModel
   ```


* 1.4.4. Pixel-wise mean and standard deviation files will be saved in Image_datasets. Prediction on N sweeps and N neuts (N = (1-splt)*Number of .ms files of the chosen class), consecutively, will be saved as 'modelName'_test_prediction.npy




2. Model testing:

* 2.1. Mode: **preprocess_vcf** dividing CSV files exported from VCF files into window based subfiles:


* 2.1.1 To view the necessary arguments, run:
   ```sh
   python TrIdent.py preprocess_VCF -h
   ```
* 2.1.2. Arguments are: fileName: file name (gzipped .vcf), outFolder: Output folder name

* 2.1.3.  Example run with sample file:

   ```sh
   python TrIdent.py -mode preprocess_vcf -fileName chrom22.vcf.gz -outFolder chr22
   ```

* 2.1.4 Output (.npy) will be saved in "VCF_datasets" folder.




* 2.2. Mode: **image_generation_vcf** geneate image dataset from parsed vcf file:


* 2.2.1 To view the necessary arguments, run:
   ```sh
   python TrIdent.py image_generation_vcf -h
   ```

* 2.2.2. Arguments are: subfolder: folder within VCF folder where subfiles are saved, nHap: number of haplotypes, pref: file prefix, start: Start number of files with the file prefix, stop: Stop number of files with the file prefix, imgDim: Image dimension. For 299 x 299, put 299, outDat: Output dataset name

* 2.2.3.  Example run with sample file:

   ```sh
   python TrIdent.py -mode image_generation_vcf -subfolder chr22 -nHap 198 -pref chrom22 -start 1 -stop 10 -imgDim 299 -outDat testVCF
   ```

* 2.2.4 Output will be saved in "VCF_datasets" folder.


* 2.3 Mode: **prediction** on empirical image dataset file: 

* 2.3.1. To view the necessary arguments, run:
   ```sh
   python TrIdent.py prediction -h
   ```

* 2.3.2. Arguments are: fileName: Name of the file to predict on, modelName: Model Name

* 2.3.3. Example run with sample empirical image dataset file:

   ```sh
   python TrIdent.py -mode prediction -fileName testVCF -modelName expModel
   ```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Sandipan Paul Arnab - sarnab2020@fau.edu



<p align="right">(<a href="#top">back to top</a>)</p>







<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Python.org]: https://data-science-blog.com/wp-content/uploads/2022/01/python-logo-header-1030x259.png
[Python-url]: https://www.python.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
