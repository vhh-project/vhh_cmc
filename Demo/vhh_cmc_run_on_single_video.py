from cmc.CMC import CMC

cmc_instance = CMC(config_file="/home/dhelm/VHH_Develop/pycharm_vhh_cmc/config/config_cmc.yaml")
cmc_instance.runOnSingleVideo(shots_per_vid_np=None, max_recall_id=2)


