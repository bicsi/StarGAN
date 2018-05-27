python main.py --mode train --dataset RaFD --rafd_crop_size 256 \
                 --image_size 256 \
                 --c_dim 2 --rafd_image_dir data/rafd \
                 --sample_dir stargan_custom/samples --log_dir stargan_custom/logs \
                 --model_save_dir stargan_custom/models \
                 --result_dir stargan_custom/results \
                 --g_conv_dim 16 \
                 --d_conv_dim 16 \
                 --g_repeat_num 2 \
                 --d_repeat_num 2 \
