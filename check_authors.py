# Author: Michael Coughlin
import os
import sys

authors = {
'Igor Andreoni': [
'Department of Physics and Astronomy, University of North Carolina at Chapel Hill, Chapel Hill, NC 27599-3255, USA',
'Joint Space-Science Institute, University of Maryland, College Park, MD 20742, USA', 'Department of Astronomy, University of Maryland, College Park, MD 20742, USA', 'Astrophysics Science Division, NASA Goddard Space Flight Center, Mail Code 661, Greenbelt, MD 20771, USA'],
"Raffaella Margutti": ["Department of Astronomy, University of California, Berkeley, CA 94720, USA", "Department of Physics, University of California, 366 Physics North MC 7300, Berkeley, CA 94720, USA"],
"John Banovetz": ["Brookhaven National Laboratory, Bldg 510, Upton, NY 11973, USA"],
"Sarah Greenstreet": ["Vera C. Rubin Observatory/NSF NOIRLab 950 N Cherry Ave., Tucson, AZ, 85749, USA", "Department of Astronomy and the DiRAC Institute, University of Washington, Seattle, WA, USA"],
"Claire-Alice Hébert": ["Brookhaven National Laboratory, Bldg 510, Upton, NY 11973, USA"],
"Tim Lister": ["Las Cumbres Observatory, 6740 Cortona Drive Ste 102, Goleta, CA, 93117, USA"],
"Antonella Palmese": ["McWilliams Center for Cosmology and Astrophysics, Department of Physics, Carnegie Mellon University, Pittsburgh, PA 15213, USA"],
"Silvia Piranomonte": ["INAF, Osservatorio Astronomico di Roma, via Frascati 33, I-00078 Monte Porzio Catone (RM), Italy"],
"S. J. Smartt": ["Department of Physics, University of Oxford, Keble Road, Oxford, OX1 3RH, UK", "Astrophysics Research Centre, School of Mathematics and Physics, Queen's University Belfast, BT7 1NN, UK"],
"Graham P. Smith": ["School of Physics and Astronomy, University of Birmingham, Birmingham B15 2TT, UK"],
"Robert Stein": ["Division of Physics, Mathematics, and Astronomy, California Institute of Technology, Pasadena, CA 91125, USA"],

"Tomas Ahumada": ["Division of Physics, Mathematics and Astronomy, California Institute of Technology, Pasadena, CA 91125, USA"],
"Shreya Anand": ["Department of Physics, Stanford University, 382 Via Pueblo Mall, Stanford, California 94305, USA", "Kavli Institute for Particle Astrophysics & Cosmology, P. O. Box 2450, Stanford University, Stanford, California 94305, USA", "SLAC National Accelerator Laboratory, Stanford University, 2575 Sand Hill Road, Menlo Park, CA 94025, USA"],
"Katie Auchettl": ["OzGrav, School of Physics, The University of Melbourne, Parkville, VIC 3010, Australia", "Department of Astronomy and Astrophysics, University of California, Santa Cruz, CA,  95064, USA"],
"Michele T. Bannister": ["School of Physical and Chemical Sciences|Te Kura Matu, University of Canterbury, Private Bag 4800, Christchurch 8140, New Zealand"],
"Eric C. Bellm": ["Department of Astronomy and the DiRAC Institute, University of Washington, Seattle, WA, USA"],
"Joshua S. Bloom": ["Department of Astronomy, University of California, Berkeley, CA 94720, USA", "Lawrence Berkeley National Laboratory, 1 Cyclotron Road, MS 50B-4206, Berkeley, CA 94720, USA"],
"Bryce T. Bolin": ["Eureka Scientific, 2452 Delmer Street, Oakland, CA 94602"],
"Clecio R. Bom": ["Centro Brasileiro de Pesquisas F´ısicas, Rua Dr. Xavier Sigaud 150, Rio de Janeiro, 22290-180, RJ, Brazil", "Centro Federal de Educacao Tecnologica Celso Suckow da Fonseca, Rodovia Marcio Covas, lote J2, quadra J, Itaguai, Brazil"],
"Daniel Brethauer": ["Department of Astronomy, University of California, Berkeley, CA 94720, USA"],
"Melissa J. Brucker": ["University of Arizona, Lunar and Planetary Laboratory, 1629 E. University Blvd.,Tucson, AZ 85721, USA"],
"David A.H. Buckley": ["South African Astronomical Observatory, PO Box 9, Observatory 7935, Cape Town, South Africa", "Department of Astronomy, University of Cape Town, Private Bag X3, Rondebosch 7701, South Africa", "Department of Physics, University of the Free State, P.O. Box 339, Bloemfontein 9300, South Africa"],
"Poonam Chandra": ["National Radio Astronomy Observatory, 520 Edgemont Rd, Charlottesville VA 22903, USA"],
"Ryan Chornock": ["Department of Astronomy, University of California, Berkeley, CA 94720, USA"],
"Eric Christensen": ["Vera C. Rubin Observatory/NSF NOIRLab 950 N Cherry Ave., Tucson, AZ, 85749, USA"],
"Jeff Cooke": ["Centre for Astrophysics and Supercomputing, Swinburne University of Technology, Hawthorn, VIC 3122, Australia", "Australian Research Council Centre of Excellence for Gravitational Wave Discovery (OzGrav), Australia"],
"Alessandra Corsi": ["Department of Physics and Astronomy, Texas Tech University, Lubbock, TX, United States"],
'Michael W. Coughlin': ['School of Physics and Astronomy, University of Minnesota, Minneapolis, Minnesota 55455, USA'],
"Bolivia Cuevas-Otahola": ["Benemérita Universidad Autónoma de Puebla, Av. San Manuel, 72000 Puebla, Mexico"],
"D'Ammando Filippo": ["INAF-IRA, Via P. Gobetti 101, I-40129, Bologna, Italy"],
"Biwei Dai": ["Department of Physics, University of California, 366 Physics North MC 7300, Berkeley, CA 94720, USA", "Lawrence Berkeley National Laboratory, 1 Cyclotron Road, MS 50B-4206, Berkeley, CA 94720, USA"],
"S. Dhawan": ["Institute of Astronomy and Kavli Institute for Cosmology, University of Cambridge, Madingley Road, Cambridge CB3 0HA, UK"],
"Alexei V. Filippenko": ["Department of Astronomy, University of California, Berkeley, CA 94720, USA"],
"Ryan J. Foley": ["Department of Astronomy and Astrophysics, University of California, Santa Cruz, CA,  95064, USA"],
"Anna Franckowiak": ["Ruhr University Bochum, Faculty of Physics and Astronomy, Astronomical Institute (AIRUB), Universitätsstraße 150, 44801 Bochum, Germany"],
"Andreja Gomboc": ["Center for Astrophysics and Cosmology, University of Nova Gorica, Vipavska 13, 5000 Nova Gorica, Slovenia"],
"Benjamin P. Gompertz": ["School of Physics and Astronomy, University of Birmingham, Birmingham B15 2TT, UK", "Institute for Gravitational Wave Astronomy, University of Birmingham, Birmingham B15 2TT, UK"],
"Leanne P. Guy": ["Vera C. Rubin Observatory/NSF NOIRLab 950 N Cherry Ave., Tucson, AZ, 85749, USA"],
"Nandini Hazra": ["Gran Sasso Science Institute (GSSI) L'Aquila, Italy", "INAF-Astronomical Observatory of Abruzzo, Via Maggini snc, 64020, Teramo, Italy", "INFN Laboratori Nazionali del Gran Sasso, L'Aquila, Italy"],
"Christopher Hernandez": ["Department of Physics and Astronomy, University of Pittsburgh, 3941 O’Hara St, Pittsburgh, PA 15260"],
"Griffin Hosseinzadeh": ["Department of Astronomy & Astrophysics, University of California, San Diego, 9500 Gilman Drive, MC 0424, La Jolla, CA 92093-0424, USA"],
"Maryam Hussaini": ["Center for Astrophysics | Harvard & Smithsonian, 60 Garden Street, Cambridge, MA 02138-1516, USA"],
"Dina Ibrahimzade": ["Department of Astronomy, University of California, Berkeley, CA 94720, USA"],
"Luca Izzo": ["INAF, Osservatorio Astronomico di Capodimonte, Salita Moiariello 16, I-80131 Napoli, Italy", "DARK, Niels Bohr Institute, University of Copenhagen, Jagtvej 128, 2200 Copenhagen, Denmark"],
"R. Lynne Jones": ["Vera C. Rubin Observatory/NSF NOIRLab 950 N Cherry Ave., Tucson, AZ, 85749, USA"],
"Yijung Kang": ["Kavli Institute for Particle Astrophysics & Cosmology, P. O. Box 2450, Stanford University, Stanford, California 94305, USA", "SLAC National Accelerator Laboratory, Stanford University, 2575 Sand Hill Road, Menlo Park, CA 94025, USA"],
"Mansi M. Kasliwal": ["Division of Physics, Mathematics, and Astronomy, California Institute of Technology, Pasadena, CA 91125, USA"],
"Matthew Knight": ["United States Naval Academy"],
"Keerthi Kunnumkai": ["McWilliams Center for Cosmology and Astrophysics, Department of Physics, Carnegie Mellon University, Pittsburgh, PA 15213, USA"],
"Gavin P Lamb": ["Astrophysics Research Institute, Liverpool John Moores University, IC2 Liverpool Science Park, 146 Brownlow Hill, Liverpool, L3 5RF, UK"],
"Natalie LeBaron": ["Department of Astronomy, University of California, Berkeley, CA 94720, USA"],
"Cassandra Lejoly": ["University of Arizona, Lunar and Planetary Laboratory, 1629 E. University Blvd.,Tucson, AZ 85721, USA"],
"Andrew J. Levan": ["Department of Astrophysics, Institute for Mathematics, Astrophysics and Particle Physics (IMAPP), Radboud University, Nijmegen, The Netherlands", "Department of Physics, University of Warwick, Coventry, UK"],
"Sean MacBride": ["Physik-Institut, University of Zurich, Winterthurerstrasse 190, 8057 Zurich, Switzerland"],
"Franco Mallia": ["Campo Catino Astronomical Observatory, Regione Lazio, Guarcino (FR), 03010, Italy"],
"Alex I. Malz": ["McWilliams Center for Cosmology and Astrophysics, Department of Physics, Carnegie Mellon University, Pittsburgh, PA, USA"],
"Adam A. Miller": ["Department of Physics and Astronomy, Northwestern University, 2145 Sheridan Rd, Evanston, IL 60208, USA", "Center for Interdisciplinary Exploration and Research in Astrophysics (CIERA), Northwestern University, 1800 Sherman Ave, Evanston, IL 60201, USA"],
"John Carlos Mora (J. C. Mora)": ["EXPOASTRONOMY Astrophysics and Space Sciences Research Group, Global Sky Partner of Las Cumbres Observatory", "University of Chile", "Inter-University Centre for Astronomy and Astrophysics (IUCAA)"],
"Gautham Narayan": ["University of Illinois, Urbana-Champaign, Dept. of Astronomy, 1002 W. Green St., Urbana, IL 61801, USA", "Center for AstroPhysical Surveys, NCSA, 1205 W Clark St, Urbana, IL 61801, USA"],
"Nayana A.J.": ["Department of Astronomy, University of California, Berkeley, CA 94720, USA"],
"Matt Nicholl": ["Astrophysics Research Centre, School of Mathematics and Physics, Queens University Belfast, Belfast BT7 1NN, UK"],
"Tiffany Nichols": ["Princeton University, Department of Astrophysical Sciences", "Legacy Survey of Space and Time Discovery Alliance Catalyst Fellow", "Princeton University, Department of History"],
"S. R. Oates": ["Department of Physics, Lancaster University, Lancaster, LA1 4YB, UK"],
"Akshay Panayada": ["Center for Machine Intelligence and Data science (C-MInDS), IIT Bombay, India"],
"Fabio Ragosta": ["Dipartimento di Fisica “E. Pancini”, Università di Napoli “Federico II”, Via Cinthia 21, I-80126 Napoli, Italy", "INAF – Osservatorio Astronomico di Capodimonte, Salita Moiariello 16, I-80131 Napoli, Italy"],
"Tiago Ribeiro": ["Vera C. Rubin Observatory/NSF NOIRLab 950 N Cherry Ave., Tucson, AZ, 85749, USA"],
"Dan Ryczanowski": ["Institute of Cosmology and Gravitation, University of Portsmouth, Burnaby Rd, Portsmouth, PO1 3FX, UK", "School of Physics and Astronomy, University of Birmingham, Birmingham B15 2TT, UK"],
"Nikhil Sarin": ["Oskar Klein Centre for Cosmoparticle Physics, Department of Physics, Stockholm University, AlbaNova, Stockholm SE-106 91, Sweden", "Nordita, Stockholm University and KTH Royal Institute of Technology, Hannes Alfvéns väg 12, SE-106 91 Stockholm, Sweden"],
"Megan E. Schwamb": ["Astrophysics Research Centre, School of Mathematics and Physics, Queen's University Belfast, Belfast BT7 1NN, UK"],
"Huei Sears": ["Department of Physics and Astronomy, Rutgers, the State University of New Jersey, 136 Frelinghuysen Road, Piscataway, NJ 08854-8019, USA"],
"Darryl Z. Seligman": ["Department of Astronomy and Carl Sagan Institute, Cornell University, 122 Sciences Drive, Ithaca, NY, 14853, USA", "NSF Astronomy and Astrophysics Postdoctoral Fellow"],
"Ritwik Sharma": ["Institut für Physik und Astronomie, Universität Potsdam, Haus 28, Karl-Liebknecht-Str. 24/25, 14476 Potsdam, Germany."],
"Manisha Shrestha": ["Steward Observatory, University of Arizona, 933 North Cherry Avenue, Tucson, AZ 85721-0065, USA"],
"Simran Kaur": ["Department of Physics, University of Michigan, Ann Arbor, MI 48109 USA"],
"Michael C. Stroh": ["Center for Interdisciplinary Exploration and Research in Astrophysics (CIERA), Northwestern University, 1800 Sherman Ave, Evanston, IL 60201, USA"],
"Giacomo Terreran": ["Las Cumbres Observatory, 6740 Cortona Drive Ste 102, Goleta, CA, 93117, USA"],
"Aishwarya Linesh Thakur": ["INAF-Istituto di Astrofisica e Planetologia Spaziali, via Fosso del Cavaliere, 100, I-00133 Rome RM, Italy"],
"Aum Trivedi": ["International Centre for Space and Cosmology, School of Arts and Sciences, Ahmedabad University, Navrangpura, Ahmedabad, 380009, India"],
"J. Anthony Tyson": ["Department of Physics and Astronomy, University of California, One Shields Avenue, Davis, CA 95616, USA"],
"Yousuke Utsumi": ["SLAC National Accelerator Laboratory, 2575 Sand Hill Road, Menlo Park, CA 94025, USA"],
"Aprajita Verma": ["Sub-department of Astrophysics, Denys Wilkinson Building, University of Oxford, Keble Road, Oxford, OX1 3RH, U.K."],
"V. Ashley Villar": ["Center for Astrophysics | Harvard & Smithsonian, 60 Garden Street, Cambridge, MA 02138-1516, USA", "The NSF AI Institute for Artificial Intelligence and Fundamental Interactions"],
"Kathryn Volk": ["Planetary Science Institute, 1700 East Fort Lowell, Suite 106, Tucson, AZ 85719, USA"],
"Meet J. Vyas": ["International Centre for Space and Cosmology, School of Arts and Sciences, Ahmedabad University, Navrangpura, Ahmedabad, 380009, India"],
"Amanda R. Wasserman": ["University of Illinois, Urbana-Champaign, Dept. of Astronomy, 1002 W. Green St., Urbana, IL 61801, USA", "Center for AstroPhysical Surveys, NCSA, 1205 W Clark St, Urbana, IL 61801, USA"],
"J. Craig Wheeler": ["Department of Astronomy, University of Texas at Austin, Austin, TX, USA"],
"Peter Yoachim": ["Department of Astronomy and the DiRAC Institute, University of Washington, Seattle, WA, USA"],
"Angela Zegarelli": ["Ruhr University Bochum, Faculty of Physics and Astronomy, Astronomical Institute (AIRUB), Universitätsstraße 150, 44801 Bochum, Germany"],
"Federica Bianco": ["University of Delaware Department of Physics and Astronomy 217 Sharp Lab Newark, DE 19716 USA", "University of Delaware Joseph R. Biden, Jr. School of Public Policy and Administration, 184 Academy St, Newark, DE 19716 USA", "University of Delaware Data Science Institute", "Center for Urban Science and Progress, New York University, 370 Jay St, Brooklyn, NY 11201, USA"],
    }

institution_list_ordered = []
for key in authors.keys():
    instutions = authors[key]
    for instution in instutions:
        if instution in institution_list_ordered: continue
        institution_list_ordered.append(instution)

author_list = []
author_list_arxiv = []
for key in authors.keys():
    author_institutions = authors[key]
    indices = []
    for author_institution in author_institutions:
        indices.append(institution_list_ordered.index(author_institution))
    author_list.append('%s (%s)' % (key, ",".join([str(x+1) for x in indices])))
    author_list_arxiv.append(key)

#print(", ".join(author_list_arxiv))

print(", ".join(author_list))

#institution_list = []
#for ii, institution in enumerate(institution_list_ordered):
#    institution_list.append('$^{%s}$ %s' % (str(ii+1), institution))
#print("\n".join(institution_list)) 
#
#print("--------")
institution_list = []
for ii, institution in enumerate(institution_list_ordered):
    institution_list.append('(%s) %s' % (ii+1, institution))
print("\n".join(institution_list))

print('--------')
print(f"Total {len(authors)} authors") 
