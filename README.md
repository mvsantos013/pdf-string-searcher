# PDF String Searcher
This Python 2.7 project is useful for searching an expression in a local/remote PDF.

# Features
This project provides a way to search for an expression in a PDF file, it can be a local file or a online one. You can do it via coding as explained in [this example](https://github.com/mvsantos013/pdf-string-searcher/blob/master/src/example.py) or using the Tkinter [simple interface](https://github.com/mvsantos013/pdf-string-searcher/blob/master/src/gui.py) with logging to make things easier. It uses pdfminer module to read PDF files, some changes were made to increase perfomance, it can also read a wide range of PDFs with embedded/subsetted fonts.

# Explaining user interface
You have a basic interface with only two input fields:
- Link
  - This is a url of a webpage, it can be a normal page or a PDF one. If it is a normal page the algorithm will look for every PDF link at the page and search for the expression in each one of them. If it is a PDF page it will search for the expression in that PDF only.
- Expression
  - This is a text that you want to search in the PDFs, it is case insensitive, in other words, the expression "nAmE" is the same as "NAME".
  
<p align="center">
  <img src="https://github.com/mvsantos013/pdf-string-searcher/blob/master/resources/imgs/pdf-string-searcher-gui.png?raw=true">
</p>
