#!/usr/bin/env perl
$latex            = 'uplatex -shell-escape -synctex=1 -halt-on-error';
$latex_silent     = 'uplatex -shell-escape -synctex=1 -halt-on-error -interaction=batchmode';
$bibtex           = 'upbibtex %O %B';
$biber            = 'biber %O --bblencoding=utf8 -u -U --output_safechars %B';
$dvipdf           = 'dvipdfmx %O -o %D %S';
#$makeindex        = 'upmendex %O -o %D %S';
$max_repeat       = 5;
$pdf_mode         = 3;
