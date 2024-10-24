#*********************************************************************************
#* Copyright (C) 2024 Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 3 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#***********************************************************************************
"""
.. module:: Phenol
   :platform: Unix, Windows
   :synopsis: This module implements the 3-state 2D model Hamiltonian of phenol molecule
.. moduleauthor:: Alexey V. Akimov

"""

import os
import sys
import math
import copy

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
import util.libutil as comn
import libra_py.units as units


class tmp:
    pass




def Pollin_Arribas_Agostini(q, _params, full_id=None):
    """
    Model as described here:
    Pollien, A.; Villaseco Arribas, E.; Lauvergnat, D.; Agostini, F. 
    Exact-Factorisation Study of the Photochemistry of Phenol. Molecular Physics 0 (0), 
    e2378960. https://doi.org/10.1080/00268976.2024.2378960.
  
    Coded with the assistance of ChatGPT

    Args:
        q ( MATRIX(ndof, ntraj) ): coordinates of all the particles, ndof should be = 2

        params ( dictionary ): model parameters, should contain:


    Returns:
        PyObject: obj, with the members:

            * obj.ham_dia ( CMATRIX(3,3) ): diabatic Hamiltonian
            * obj.ovlp_dia ( CMATRIX(3,3) ): overlap of the basis (diabatic) states [ identity ]
            * obj.d1ham_dia ( list of 2 CMATRIX(3,3) objects ): derivatives of the diabatic Hamiltonian w.r.t. the nuclear coordinate
            * obj.dc1_dia ( list of 2 CMATRIX(nstates,nstates) objects ): derivative coupling in the diabatic basis [ zero ]

    """


    params = dict(_params)

    # Define potential specific constants
    critical_params = ["nstates"]
    default_params = { }
    comn.check_input(params, default_params, critical_params)

    ndof = q.num_of_rows  # the number of nuclear DOFs
    nstates = params["nstates"]

    if ndof!=2:
        print(F"The number of DOFs should be 2 but {ndof} is given\n" )
        sys.exit(0);
    if nstates!=3:
        print(F"The number of states should be 3, but {nstates} is given\n")
        sys.exit(0);

    # Constants:
    # Conversion factors to atomic units
    eV_to_au = 0.0367493  # 1 eV = 0.0367493 Hartree
    A_to_au = 1.88973  # 1 Angstrom = 1.88973 Bohr
    amu_to_au = 1822.8885  # 1 atomic mass unit = 1822.8885 atomic units

    # Constants and parameters in atomic units
    D1e = 4.26302 * eV_to_au  # eV to atomic units (Hartree)
    D3e = 4.47382 * eV_to_au  # eV to atomic units (Hartree)
    a1 = 2.66021 / A_to_au  # Å^-1 to Bohr^-1
    a3 = 2.38671 / A_to_au  # Å^-1 to Bohr^-1
    r1 = 0.96944 * A_to_au  # Å to Bohr
    r3 = 0.96304 * A_to_au  # Å to Bohr
    a30 = 4.85842 * eV_to_au  # eV to atomic units (Hartree)

    A1 = 0.27037 * eV_to_au  # eV to atomic units (Hartree)
    A2 = 1.96606 * A_to_au  # Å to Bohr
    A3 = 0.685264 * A_to_au  # Å to Bohr
    C1 = 0.110336 * eV_to_au  # eV to atomic units (Hartree)
    C2 = 1.21724 * A_to_au  # Å to Bohr
    C3 = 0.06778 * A_to_au  # Å to Bohr

    B201 = 0.192205 * eV_to_au  # eV to atomic units (Hartree)
    B202 = 5.67356 / A_to_au  # Å^-1 to Bohr^-1
    B203 = 1.03171 * A_to_au  # Å to Bohr
    B204 = 5.50696 * eV_to_au  # eV to atomic units (Hartree)

    B205 = 4.70601 * eV_to_au  # eV to atomic units (Hartree)
    B206 = 2.49826 / A_to_au  # Å^-1 to Bohr^-1
    B207 = 0.988188 * A_to_au  # Å to Bohr
    B208 = 3.3257 * eV_to_au  # eV to atomic units (Hartree)

    lambda_12_max = 1.47613 * eV_to_au  # eV to atomic units (Hartree)
    d12 = 1.96984 * A_to_au  # Å to Bohr
    beta12 = 0.494373 * A_to_au  # Å to Bohr

    lambda_23_max = 0.327204 * eV_to_au  # eV to atomic units (Hartree)
    d23 = 1.22594 * A_to_au  # Å to Bohr
    beta23 = 0.0700604 * A_to_au  # Å to Bohr

    chi20 = 0.326432 * eV_to_au**2  # eV^2 to Hartree^2
    chi21 = 0.021105 * eV_to_au**2  # eV^2 to Hartree^2
    chi22 = 0.0  # eV^2 to Hartree^2

    B211 = -0.2902 * eV_to_au  # eV to atomic units (Hartree)
    B212 = 2.05715 * A_to_au  # Å to Bohr
    B213 = 1.01574 * A_to_au  # Å to Bohr

    B214 = -73.329 * eV_to_au  # eV to atomic units (Hartree)
    B215 = 1.48285 * A_to_AU  # Å to AU
    B216 = -0.1111 * A_to_AU  # Å to AU
    B217 = -0.00055 * eV_to_AU  # eV to AU

    B221 = 27.3756 * eV_to_AU  # eV to AU
    B222 = 1.66881 * A_to_AU  # Å to AU
    B223 = 0.20557 * A_to_AU  # Å to AU
    B224 = 0.35567 * eV_to_AU  # eV to AU
    B225 = 1.43492 * A_to_AU  # Å to AU
    B226 = 0.56968 * A_to_AU  # Å to AU

    rCC = 1.39403 * A_to_AU  # Å to AU
    rCH = 1.08441 * A_to_AU  # Å to AU
    alpha = 109.1333  # degrees (no conversion needed)

    # 1 kg = 6.02214 × 10^26 atomic mass unit (AMU); 1 AMU = 1822.888486 atomic units of mass
    # so 1 kg = 1.09777 x 10^30 atomic units 
    mu_OH = 1728.5 #  1.57456e-27 kg to atomic units (mass)


    # Get the coordinates:
    indx = 0
    if full_id !=None:
        Id = Cpp2Py(full_id)
        indx = Id[-1]

    r = q.get(0, indx)
    theta = q.get(1, indx)

    # Defining the functions as per the equations
    x = np.exp(-a1 * (r - r1)); dx_dr = -a1*x;
    v10 = D1e * (1 - x)**2; dv10_dr = -2.0*D1e*(1-x)*dx_dr
    x = np.tanh((r - A2) / A3);  dx_dr = (1 - x**2)/A3
    v11 = 0.5 * A1 * (1 - x);    dv11_dr = -0.5*A1*dx_dr

    x = np.exp(-B202 * (r - B203)); dx_dr = -B202*x;
    v201 = B201 * (1 - x)**2 + B204;   dv201_dr = -2.0 * B201*(1.0 - x)* dx_dr;
    x = np.exp(-B206 * (r - B207));   dx_dr = -B206 * x
    v202 = B205 * x + B208;  dv202_dr = B205 * dx_dr
    x = np.sqrt((v201 - v202)**2 + chi20); dx_dr = (v201 - v202)*(dv201_dr - dv202_dr)/x;
    v20 = 0.5 * (v201 + v202) - 0.5 * x;  dv20_dr = 0.5 * (dv201_dr + dv202_dr) - 0.5*dx_dr

    x = np.tanh((r - B212) / B213); dx_dr = (1.0 - x**2)/B213;
    v211 = 0.5 * B211 * (1 - x); dv211_dr = -2.0*B211 *dx_dr;
    x = np.tanh((r - B215) / B216); dx_dr = (1.0 - x**2)/B216;
    v212 = 0.5 * B214 * (1 - x) + B217; dv212 = -2.0*B214*dx_dr;
    x = np.sqrt((v211 - v212)**2 + chi21); dx_dr = (v211 - v212)*(dv211_dr - dv212_dr)/x;
    v21 = 0.5 * (v211 + v212) - 0.5 * x;  dv21_dr = 0.5 * (dv211_dr + dv212_dr) - 0.5*dx_dr

    x = np.tanh((r - B222) / B223)); dx_dr = (1.0 - x**2)/B223
    v221 = 0.5 * B221 * (1 + x); dv221_dr = 0.5 * B221 * dx_dr;
    x = np.tanh((r - B225) / B226); dx_dr = (1.0 - x**2)/B226
    v222 = 0.5 * B224 * (1 - x); dv222_dx = -0.5 * B224 * dx_dr; 
    x = np.sqrt((v221 - v222)**2 + chi22); dx_dr = (v221 - v222)*(dv221_dr - dv222_dr)/x;
    v22 = 0.5 * (v221 + v222) - 0.5 * x;  dv22_dr = 0.5 * (dv221_dr + dv222_dr) - 0.5*dx_dr

    x = np.exp(-a3 * (r - r3)); dx_dr = -a3 * x;
    v30 = D3e * (1 - x)**2 + a30; dv30_dr = D3e * 2.0 * (1.0 - x)*dx_dr; 
    x = np.tanh((r - C2) / C3); dx_dr = (1.0 - x**2)/C3; 
    v31 = 0.5 * C1 * (1 - x); dv31_dr = -0.5 * C1 * dx_dr

    # Off-diagonal elements
    cs = np.cos(theta);
    si = np.sin(theta);
    cs2 = np.cos(2.0 * theta)
    si2 = np.sin(2.0 * theta)

    x =  np.tanh((r - d12) / beta12); dx_dr = (1.0 - x**2)/beta12;
    lambda_12_r = 0.5 * lambda_12_max * (1 - x); dlambda_12_r_dr = -0.5 * lambda_12_max * dx_dr
    V12 = lambda_12_r * si; dV12_dr = dlambda_12_r_dr * si; dV12_dtheta = lambda_12_r * cs;

    V13 = 0.0

    x = np.tanh((r - d23) / beta23); dx_dr = (1.0 - x**2)/beta23;
    lambda_23_r = 0.5 * lambda_23_max * (1 - x); dlambda_23_r_dr = -0.5 * lambda_23_max * dx_dr;
    V23 = lambda_23_r * si; dV23 = dlambda_23_r_dr * si; dV23_dtheta = lambda_23_r * cs;


    # Diagonal elements of Hamiltonian
    V11 = v10 + v11 * (1 - cs2)
    V22 = v20 + v21 * (1 - cs2) + v22 * (1 - cs2)**2
    V33 = v30 + v31 * (1 - cs2)

    dV11_dr = dv10_dr + dv11_dr * (1 - cs2);  dV11_dtheta = 2.0 * v11 * si2;  
    dV22_dr = dv20_dr + dv21_dr * (1 - cs2) + dv22_dr * (1 - cs2)**2;  dV22_dtheta = 2.0 * v21 * si2 - 4.0 * v22 * (1 - cs2) * si2;
    dV33_dr = dv30_dr + dv31_dr * (1 - cs2);  dV33_dtheta = 2.0 * v31 * si2;

   

    obj = tmp()
    obj.ham_dia = CMATRIX(3, 3)
    obj.ovlp_dia = CMATRIX(3, 3);  obj.ovlp_dia.identity()
    obj.d1ham_dia = CMATRIXList()
    obj.dc1_dia = CMATRIXList()


    for i in range(2):
        obj.d1ham_dia.append( CMATRIX(3, 3) )
        obj.dc1_dia.append( CMATRIX(3, 3) )



    #=========== Energies & Derivatives ===============
    # Hamiltonian matrix
    obj.ham_dia.set(0,0, V11*(1.0+0.0j));  obj.ham_dia.set(0,1, V12*(1.0+0.0j)); obj.ham_dia.set(0,2, V13*(1.0+0.0j));
    obj.ham_dia.set(1,0, V12*(1.0+0.0j));  obj.ham_dia.set(1,1, V22*(1.0+0.0j)); obj.ham_dia.set(1,2, V23*(1.0+0.0j));
    obj.ham_dia.set(2,0, V13*(1.0+0.0j));  obj.ham_dia.set(2,1, V23*(1.0+0.0j)); obj.ham_dia.set(2,2, V33*(1.0+0.0j));

    # Derivatives with respect to r
    obj.d1ham_dia[0].set(0,0, dV11_dr*(1.0+0.0j));  
    obj.d1ham_dia[0].set(0,1, dV12_dr*(1.0+0.0j)); 
    obj.d1ham_dia[0].set(0,2, dV13_dr*(1.0+0.0j));
    
    obj.d1ham_dia[0].set(1,0, dV12_dr*(1.0+0.0j));  
    obj.d1ham_dia[0].set(1,1, dV22_dr*(1.0+0.0j)); 
    obj.d1ham_dia[0].set(1,2, dV23_dr*(1.0+0.0j));
    
    obj.d1ham_dia[0].set(2,0, dV13_dr*(1.0+0.0j));  
    obj.d1ham_dia[0].set(2,1, dV23_dr*(1.0+0.0j)); 
    obj.d1ham_dia[0].set(2,2, dV33_dr*(1.0+0.0j));


    # Derivatives with respect to theta
    obj.d1ham_dia[1].set(0,0, dV11_dtheta*(1.0+0.0j));
    obj.d1ham_dia[1].set(0,1, dV12_dtheta*(1.0+0.0j));
    obj.d1ham_dia[1].set(0,2, dV13_dtheta*(1.0+0.0j));

    obj.d1ham_dia[1].set(1,0, dV12_dtheta*(1.0+0.0j));
    obj.d1ham_dia[1].set(1,1, dV22_dtheta*(1.0+0.0j));
    obj.d1ham_dia[1].set(1,2, dV23_dtheta*(1.0+0.0j));

    obj.d1ham_dia[1].set(2,0, dV13_dtheta*(1.0+0.0j));
    obj.d1ham_dia[1].set(2,1, dV23_dtheta*(1.0+0.0j));
    obj.d1ham_dia[1].set(2,2, dV33_dtheta*(1.0+0.0j));


    return obj

