# BSD 3-Clause License
#
# Copyright (c) 2022, FourCastNet authors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The code was authored by the following people:
#
# Jaideep Pathak - NVIDIA Corporation
# Shashank Subramanian - NERSC, Lawrence Berkeley National Laboratory
# Peter Harrington - NERSC, Lawrence Berkeley National Laboratory
# Sanjeev Raja - NERSC, Lawrence Berkeley National Laboratory
# Ashesh Chattopadhyay - Rice University
# Morteza Mardani - NVIDIA Corporation
# Thorsten Kurth - NVIDIA Corporation
# David Hall - NVIDIA Corporation
# Zongyi Li - California Institute of Technology, NVIDIA Corporation
# Kamyar Azizzadenesheli - Purdue University
# Pedram Hassanzadeh - Rice University
# Karthik Kashinath - NVIDIA Corporation
# Animashree Anandkumar - California Institute of Technology, NVIDIA Corporation


# Instructions:
# Set Nimgtot correctly

import h5py
from mpi4py import MPI
import numpy as np
import time
from netCDF4 import Dataset as DS
import os

def writetofile(src, dest, channel_idx, varslist, src_idx=0, frmt='nc'):
    if os.path.isfile(src):
        batch = 2**4
        rank = MPI.COMM_WORLD.rank
        Nproc = MPI.COMM_WORLD.size
        Nimgtot = 52#src_shape[0]

        Nimg = Nimgtot//Nproc
        base = rank*Nimg
        end = (rank+1)*Nimg if rank<Nproc - 1 else Nimgtot
        idx = base

        for variable_name in varslist:

            if frmt == 'nc':
                fsrc = DS(src, 'r', format="NETCDF4").variables[variable_name]
            elif frmt == 'h5':
                fsrc = h5py.File(src, 'r')[varslist[0]]
            print("fsrc shape", fsrc.shape)
            fdest = h5py.File(dest, 'a')

            start = time.time()
            while idx<end:
                if end - idx < batch:
                    if len(fsrc.shape) == 4:
                        ims = fsrc[idx:end,src_idx]
                    else:
                        ims = fsrc[idx:end]
                    print(ims.shape)
                    fdest['fields'][idx:end, channel_idx, :, :] = ims
                    break
                else:
                    if len(fsrc.shape) == 4:
                        ims = fsrc[idx:idx+batch,src_idx]
                    else:
                        ims = fsrc[idx:idx+batch]
                    #ims = fsrc[idx:idx+batch]
                    print("ims shape", ims.shape)
                    fdest['fields'][idx:idx+batch, channel_idx, :, :] = ims
                    idx+=batch
                    ttot = time.time() - start
                    eta = (end - base)/((idx - base)/ttot)
                    hrs = eta//3600
                    mins = (eta - 3600*hrs)//60
                    secs = (eta - 3600*hrs - 60*mins)

            ttot = time.time() - start
            hrs = ttot//3600
            mins = (ttot - 3600*hrs)//60
            secs = (ttot - 3600*hrs - 60*mins)
            channel_idx += 1
# filestr = 'oct_2021_19_31'
# dest = './global/cscratch1/sd/jpathak/21var/oct_2021_19_21.h5'
#
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_sfc.nc'
# #u10 v10 t2m
# writetofile(src, dest, 0, ['u10'])
# writetofile(src, dest, 1, ['v10'])
# writetofile(src, dest, 2, ['t2m'])
#
# #sp mslp
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_sfc.nc'
# writetofile(src, dest, 3, ['sp'])
# writetofile(src, dest, 4, ['msl'])
#
# #t850
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc'
# writetofile(src, dest, 5, ['t'], 2)
#
# #uvz1000
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc'
# writetofile(src, dest, 6, ['u'], 3)
# writetofile(src, dest, 7, ['v'], 3)
# writetofile(src, dest, 8, ['z'], 3)
#
# #uvz850
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc'
# writetofile(src, dest, 9, ['u'], 2)
# writetofile(src, dest, 10, ['v'], 2)
# writetofile(src, dest, 11, ['z'], 2)
#
# #uvz 500
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc'
# writetofile(src, dest, 12, ['u'], 1)
# writetofile(src, dest, 13, ['v'], 1)
# writetofile(src, dest, 14, ['z'], 1)
#
# #t500
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc'
# writetofile(src, dest, 15, ['t'], 1)
#
# #z50
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc'
# writetofile(src, dest, 16, ['z'], 0)
#
# #r500
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc'
# writetofile(src, dest, 17, ['r'], 1)
#
# #r850
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc'
# writetofile(src, dest, 18, ['r'], 2)
#
# #tcwv
# src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_sfc.nc'
# writetofile(src, dest, 19, ['tcwv'])
#
# #sst
# #src = '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_sfc.nc'
# #writetofile(src, dest, 20, ['sst'])

# import h5py
# import numpy as np
# import time
# from netCDF4 import Dataset as DS
# import os
#
#
# def writetofile(src, dest, channel_idx, varslist, src_idx=0, frmt="nc"):
#     if not os.path.isfile(src):
#         print(f"Source file {src} not found")
#         return
#
#     batch = 16  # 2**4
#     Nimgtot = 52  # Total number of images to process
#
#     try:
#         # Open source file
#         if frmt == "nc":
#             with DS(src, "r", format="NETCDF4") as nc_src:
#                 fsrc = nc_src.variables[varslist[0]]
#                 print("fsrc shape", fsrc.shape)
#
#                 # Open destination file
#                 with h5py.File(dest, "a") as fdest:
#                     start = time.time()
#                     idx = 0
#
#                     while idx < Nimgtot:
#                         end_idx = min(idx + batch, Nimgtot)
#
#                         # Handle 4D vs 3D data
#                         if len(fsrc.shape) == 4:
#                             ims = fsrc[idx:end_idx, src_idx].astype(np.float32)
#                         else:
#                             ims = fsrc[idx:end_idx].astype(np.float32)
#
#                         print("ims shape", ims.shape)
#
#                         # Ensure the dataset exists
#                         if "fields" not in fdest:
#                             fields_shape = (
#                                 Nimgtot,
#                                 20,
#                                 721,
#                                 1440,
#                             )  # Adjust dimensions as needed
#                             fdest.create_dataset(
#                                 "fields", fields_shape, dtype="float32"
#                             )
#
#                         # Write data
#                         fdest["fields"][idx:end_idx, channel_idx, :, :] = ims
#
#                         if end_idx == Nimgtot:
#                             break
#
#                         idx += batch
#
#                         # Calculate and print progress
#                         ttot = time.time() - start
#                         eta = (Nimgtot - idx) / (idx / ttot) if idx > 0 else 0
#                         hrs = int(eta // 3600)
#                         mins = int((eta - 3600 * hrs) // 60)
#                         secs = int(eta - 3600 * hrs - 60 * mins)
#                         print(f"Progress: {idx}/{Nimgtot}, ETA: {hrs}h {mins}m {secs}s")
#
#     except Exception as e:
#         print(f"Error processing {varslist}: {str(e)}")
#         raise
#
#
filestr = "jan_2022_01_13"
dest = "./global/cscratch1/sd/jpathak/21var/jan_2022_01_13.h5"

src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_sfc.nc"
# u10 v10 t2m
writetofile(src, dest, 0, ["u10"])
writetofile(src, dest, 1, ["v10"])
writetofile(src, dest, 2, ["t2m"])

# sp mslp
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_sfc.nc"
writetofile(src, dest, 3, ["sp"])
writetofile(src, dest, 4, ["msl"])

# t850
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_pl.nc"
writetofile(src, dest, 5, ["t"], 2)

# uvz1000
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_pl.nc"
writetofile(src, dest, 6, ["u"], 3)
writetofile(src, dest, 7, ["v"], 3)
writetofile(src, dest, 8, ["z"], 3)

# uvz850
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_pl.nc"
writetofile(src, dest, 9, ["u"], 2)
writetofile(src, dest, 10, ["v"], 2)
writetofile(src, dest, 11, ["z"], 2)

# uvz 500
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_pl.nc"
writetofile(src, dest, 12, ["u"], 1)
writetofile(src, dest, 13, ["v"], 1)
writetofile(src, dest, 14, ["z"], 1)

# t500
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_pl.nc"
writetofile(src, dest, 15, ["t"], 1)

# z50
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_pl.nc"
writetofile(src, dest, 16, ["z"], 0)

# r500
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_pl.nc"
writetofile(src, dest, 17, ["r"], 1)

# r850
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_pl.nc"
writetofile(src, dest, 18, ["r"], 2)

# tcwv
src = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_sfc.nc"
writetofile(src, dest, 19, ["tcwv"])
# #
# # dest = "../global/cscratch1/sd/jpathak/21var/oct_2021_19_21.h5"  # Modify this path
# #
# # # Create destination file if it doesn't exist
# # if not os.path.exists(dest):
# #     with h5py.File(dest, "w") as f:
# #         pass
# #
# # # Process surface variables
# # src_sfc = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_sfc.nc"
# # for idx, var in enumerate(["u10", "v10", "t2m","sp",""]):
# #     writetofile(src_sfc, dest, idx, [var])
# #
# # # Process pressure level variables
# # src_pl = "./project/projectdirs/dasrepo/ERA5/jan_2022_01_13_pl.nc"
# # writetofile(
# #     src_pl, dest, 3, ["z"], src_idx=3
# # )  # Example for one pressure level variable
