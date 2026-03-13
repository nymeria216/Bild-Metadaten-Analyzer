% !TeX document-id = {4cee0287-fdc4-4ca2-b42e-8758e9409e53}
% !TeX encoding = UTF-8
% !TeX spellcheck = de_DE

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{Bild-Metadaten-Analyzer}[2020/07/02 Prüfungsvorlage Schildbach Stefan]
\LoadClass[11pt, a4paper]{scrartcl}

\RequirePackage[l2tabu, orthodox]{nag} % Informs about obsolete package or command use

\RequirePackage[T1]{fontenc} % Font-Encoding
\RequirePackage[utf8]{inputenc} % Input-Encoding
\RequirePackage{microtype, lmodern} % Font tweaking
\RequirePackage[english, ngerman]{babel} % word wrapping and specific language decisions (quotes)
\RequirePackage{csquotes} % Improves nested quoting
\RequirePackage[german]{isodate} % Date in ISO format
\RequirePackage[defaultlines=3, all]{nowidow} % Prevent widows
\RequirePackage{marvosym} % Symbols
\RequirePackage[backend=biber,style=ieee,hyperref=true,natbib=true,sorting=none]{biblatex} % References

\RequirePackage{fullpage, geometry} % Page margins
\geometry{a4paper, % http://en.wikibooks.org/wiki/LaTeX/Page_Layout#Page_dimensions
	top=12.5mm, 
	left=25mm, 
	right=25mm, 
	bottom=12.5mm, 
	%
	hoffset=0mm,
	marginparsep=0mm,
	marginparwidth=0mm,
	%
	footskip=.5\baselineskip,
	footnotesep=.5\baselineskip,
	%
	voffset=0mm,
	headheight=\baselineskip,
	headsep=2\baselineskip,
	includeheadfoot
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Tables, Figures and Captions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{tabularx} % Better table
\RequirePackage{booktabs} % Table improvements
\RequirePackage{subcaption} % Subfigures and subtables
\RequirePackage{arydshln} % Dashed and dotted lines % Collides with longtable if loaded previously
\RequirePackage{multicol, multirow} % Multicolumns and -rows
\RequirePackage{ragged2e} % Tablecolumn improvements and additional options

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Coloring
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{color} % Colors
\RequirePackage[table]{xcolor} % Colors in tables
\RequirePackage{graphicx} % Graphics package

\definecolor{hsmwblue}{HTML}{0068B3} % Corporate Design 2019/11/08

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Footnotes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{footnote} % Footnotes for tables are placed like regular footnotes with following commands
\makesavenoteenv{tabular}
\makesavenoteenv{tabular*}
\makesavenoteenv{table}
\makesavenoteenv{table*}
\makesavenoteenv{figure}
\makesavenoteenv{figure*} 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Misc
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{enumitem} % Improves List environments
\RequirePackage{amsmath, amssymb} % Mathsymbols
\RequirePackage{hyperref} % Links within the document

\hypersetup{ % Configure hyperref colors
	colorlinks,
	linkcolor={hsmwblue},
	citecolor={hsmwblue},
	urlcolor={hsmwblue}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Header and Footer
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage[headsepline]{scrlayer-scrpage} % Header and footer with lines
\pagestyle{scrheadings} % Use this package for display and formatiing of header and footer
\clearpairofpagestyles % Remove all default fields
\renewcommand{\headfont}{\normalfont} % Set default font
\renewcommand{\sectionmark}[1]{\markright{#1}{}}
\ihead{\rightmark}
\ohead{\pagemark} % \thepage

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Patched commands and modified lengths
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Customizing indents and paragraph skips (german style)
\setlength{\parindent}{0em}
\setlength{\parskip}{\baselineskip}

% Tables
\renewcommand{\arraystretch}{1.15} % Change spacing of table rows (percentage)
\setlength{\tabcolsep}{.5em} % Change spacing of table columns (fixed)

% Patch underline-Command to smash its contents and destroy the bounding box, thus drawing a nice baseline-underline
\let\oldunderline\underline
\renewcommand{\underline}[1]{\oldunderline{\smash{#1}}}

\setitemize{noitemsep,topsep=-\baselineskip,parsep=0em,partopsep=0em,after=\vspace*{\baselineskip}}%,leftmargin=*
\setenumerate{noitemsep,topsep=-\baselineskip,parsep=0em,partopsep=0em,after=\vspace*{\baselineskip}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Default commands
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\makeatletter
	\newcommand{\Modulbezeichnung}[1]{\def\@modulename{#1}}
	\newcommand{\Anrede}[1]{\def\@nametitle{#1}}
	\newcommand{\Vorname}[1]{\def\@prename{#1}}
	\newcommand{\Nachname}[1]{\def\@surname{#1}}
	\newcommand{\Matrikelnummer}[1]{\def\@identifier{#1}}
	\newcommand{\Seminargruppe}[1]{\def\@seminargroup{#1}}
	
	\newcommand{\@safeUse}[2][<ACHTUNG: NICHT GESETZT>]{\ifx#2\@undefined#1\PackageError{Bild-Metadaten-Analyzer}{Angabe fehlt (#1)}{}\else\ifx#2\empty#1\PackageError{Bild-Metadaten-Analyzer}{Angabe fehlt (#1)}{}\else#2\fi\fi}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\makeatletter
	\title{Programmierbeleg - Bild Metadaten Analyzer}
	\subtitle{\@modulename{}}
	\author{\@surname{}, \@prename{} (\@identifier{})}
	\date{\today}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Hooks and Layouting
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\makeatletter
	\renewcommand*{\maketitle}{%
		\thispagestyle{empty}

		\begin{minipage}[t]{.6\textwidth}
			\raggedleft
			
			\vspace*{10em}
			{\Huge\textbf{\@safeUse{\@title}}}%
			
			\vspace*{10em}
			\large
			
			\@safeUse[Herr | Frau]{\@nametitle}\\[.25\baselineskip]
			\textbf{\@safeUse[<VORNAME>]{\@prename} \@safeUse[<NACHNAME>]{\@surname}}
			
			\vspace*{5em}
			Matrikelnummer:\\[.25\baselineskip]
			\textbf{\@safeUse{\@identifier}}
			
			\vspace*{5em}
			Seminargruppe:\\[.25\baselineskip]
			\textbf{\@safeUse{\@seminargroup}}
			
			\vspace*{5em}
			Modulbezeichnung:\\[.25\baselineskip]
			\textbf{\@safeUse{\@modulename}}
			
			\vspace*{5em}
			Datum:\\[.25\baselineskip]
			\textbf{\today}
		\end{minipage}
		\hfill
		\begin{minipage}{.35\textwidth}
			\includegraphics[width=\textwidth]{hsmwLogo.pdf}
		\end{minipage}
	}

	% Begin Document Hook
	\AtBeginDocument{%
		% Set PDF-Metadata
		\hypersetup{%
			pdftitle={\@title{}},%
			pdfsubject={\@subtitle{}},%
			pdfauthor={\@author{}},%
			pdfkeywords={}%
		}%
		
		\hypersetup{pageanchor=false} % Disable Hyperref for title page due to missing numbering
		
		% Maketitle automatically
		\maketitle
		\clearpage
		
		\hypersetup{pageanchor=true}
		
		\pagenumbering{roman}
		\tableofcontents
		%\listoftables
		%\listoffigures 
		
		\clearpage
		\pagenumbering{arabic}
	}

	\AtEndDocument{%
		\clearpage
		\pagenumbering{Roman}
		
		\printbibliography[heading=bibintoc,]
	}

\makeatother

\endinput