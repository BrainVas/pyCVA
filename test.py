import urllib.request
from pycva.AutoTICI import autotici
from pycva.CAVE import cave
import pydicom

autoTICI_instance = autotici.autotici()
cave_instance = cave.cave()

#AutoTICI Util/None-Containerised method
import numpy as np

dummy_image = np.array([[10, 200, 50], [30, 250, 100]], dtype=np.uint8)
print("\nOriginal dummy image:\n", dummy_image)
normalised_image = autoTICI_instance.normalize(dummy_image)
print("\nNormalized dummy image (0-255):\n", normalised_image)

#AutoTICI
# autoTICI_instance.run_autoTICI(
#          pre_image="Dockerising_HPC_Tools/autoTICI/input_images/R3418/SN3_Vap_SOP1.2.826.0.1.3680043.9.6827.2401407280984092171337075126937802959.dcm",
#          post_image="Dockerising_HPC_Tools/autoTICI/input_images/R3418/SN10_Vap_SOP1.2.826.0.1.3680043.9.6827.2619603212203373380215256193355264957.dcm",
#          occ="M1",
#          output_dir="autotici_run/",
#          model_dir = "autotici_run/",
#          motion_correction = True)



#Run [GR-001]
# autoTICI_instance.run_autoTICI(
#          pre_image="input_images/R3418/SN3_Vap_SOP1.2.826.0.1.3680043.9.6827.2401407280984092171337075126937802959.dcm",
#          post_image="input_images/R3418/SN10_Vap_SOP1.2.826.0.1.3680043.9.6827.2619603212203373380215256193355264957.dcm",
#          occ="ICA",
#          output_dir="GR-001\packaged_2nd_run",
#          model_dir = "GR-001\packaged",
#          motion_correction = True)



#Run [GR-002]
autoTICI_instance.run_autoTICI(
         pre_image="input_images/R0160/SN4_Vap_SOP1.3.6.1.4.1.40744.9.96512919107112378459801894939320275800.dcm",
         post_image="input_images/R0160/SN48_Vap_SOP1.3.6.1.4.1.40744.9.240652218335563114333841994061787237987.dcm",
         occ="M1",
         output_dir="autotici_run",
         model_dir = "autotici_run")



#Phase predict
autoTICI_instance.run_phase_predict("input_images/R3418/SN3_Vap_SOP1.2.826.0.1.3680043.9.6827.2401407280984092171337075126937802959.dcm"
                                        , "autotici_run/"
                                        , "autotici_run/")


#-------------------------------------------------------------------------------------------------------------------------------------

#Cave
# cave_instance.run_cave( input_dicom_dir="input_images\R3418",        
#                         output_masks_dir="cave_run",           
#                         checkpoints_dir="checkpoints",
#                         input_file ="SN3_Vap_SOP1.2.826.0.1.3680043.9.6827.2401407280984092171337075126937802959.dcm",
#                         output_file = "output_mask.png",
#                         model_file = "minip_av_sigmoid_image1024_valiant-resonance-1199.pt",
#                         input_type ="minip",
#                         label_type = "av" ,
#                         img_size = 1024               
#                     )



#Run [GR-003]
# cave_instance.run_cave( input_dicom_dir="input_images\R3418",        
#                         output_masks_dir="GR-003\packaged_2nd_run",           
#                         checkpoints_dir="checkpoints_003",
#                         input_file ="SN10_Vap_SOP1.2.826.0.1.3680043.9.6827.2619603212203373380215256193355264957.dcm",
#                         output_file = "output_mask.png",
#                         model_file = "minip_vessel_sigmoid_image1024_solar-resonance-1172.pt",
#                         input_type ="minip",
#                         label_type = "vessel",
#                         img_size = 1024               
#                     )



#Run [GR-004]
cave_instance.run_cave( input_dicom_dir="input_images\R3418",        
                        output_masks_dir="cave_run",           
                        checkpoints_dir="checkpoints",
                        input_file ="SN10_Vlateral_SOP1.2.826.0.1.3680043.9.6827.1857191185591698678852008779522016086.dcm",
                        output_file = "output_mask.png",
                        model_file = "minip_av_sigmoid_image1024_valiant-resonance-1199.pt",
                        input_type ="minip",
                        label_type = "av",
                        img_size = 1024               
                    )



#Cave Util/Non-containerised method
ds = pydicom.dcmread("input_images\R0160\SN4_Vap_SOP1.3.6.1.4.1.40744.9.96512919107112378459801894939320275800.dcm")
img = ds.pixel_array

seq = np.stack([img]*25, axis=0)

print("\nsequence shape before\n", seq.shape[0])
maxLength = 20

result = cave_instance.cut_seq(seq, maxLength)
print("\nresult of cut sequence\n", result.shape[0])
