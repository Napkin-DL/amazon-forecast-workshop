import os
import torch
import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ray import tune

from neuralforecast.auto import AutoNHITS, AutoNBEATS, AutoLSTM
from neuralforecast.core import NeuralForecast

from neuralforecast.losses.pytorch import MAE
from neuralforecast.losses.numpy import mae, mse
from datasetsforecast.long_horizon import LongHorizon

import logging
logging.getLogger("pytorch_lightning").setLevel(logging.WARNING)

def arg_setting():
    parser = argparse.ArgumentParser(description='[Informer] Long Sequences Forecasting')

    parser.add_argument('--horizon', type=int, default=336, help='forecasting horizon')
    parser.add_argument('--num_samples', type=int, default=5, help='number of configurations explored')
    parser.add_argument('--freq', type=str, default='H', help='data frequency')
    parser.add_argument('--data_dir', type=str, default='./data/amzforecast/', help='data file')
    parser.add_argument('--model_dir', type=str, default='./model', help='store result')
    parser.add_argument('--cv_use', type=lambda s:s.lower() in ['true', 't', 'yes', '1'], help='cross validation', default=False)
    args = parser.parse_args()
    return args


def prepare_dataset(args):
    train_df = pd.read_csv(f'{args.data_dir}/target_train.csv')
    test_df = pd.read_csv(f'{args.data_dir}/target_test.csv')
    related_df = pd.read_csv(f'{args.data_dir}/related.csv')
    
    data = pd.merge(train_df, related_df, on=['timestamp', 'item_id'], how='left')
    data['timestamp'] = data['timestamp'].astype('datetime64[ns]')
    # data['item_id'] = data['item_id'].astype('category')
    # data['item_id'] = data['item_id'].values.codes
    data.rename(columns = {'timestamp':'ds'},inplace=True)
    data.rename(columns = {'item_id':'unique_id'},inplace=True)
    data.rename(columns = {'demand':'y'},inplace=True)

    return data

    
def set_nhits_config(args):

    # Use your own config or AutoNHITS.default_config
    nhits_config = {
           "learning_rate": tune.choice([1e-3]),                                     # Initial Learning rate
           "max_steps": tune.choice([1000]),                                         # Number of SGD steps
           "input_size": tune.choice([args.horizon, args.horizon*2, args.horizon*3, args.horizon*5]),  # input_size = multiplier * horizon
           "batch_size": tune.choice([7]),                                           # Number of series in windows
           "windows_batch_size": tune.choice([256]),                                 # Number of windows in batch
           "n_pool_kernel_size": tune.choice([[2, 2, 2], [16, 8, 1]]),               # MaxPool's Kernelsize
           "n_freq_downsample": tune.choice([[168, 24, 1], [24, 12, 1], [1, 1, 1]]), # Interpolation expressivity ratios
           "activation": tune.choice(['ReLU']),                                      # Type of non-linear activation
           "n_blocks":  tune.choice([[1, 1, 1]]),                                    # Blocks per each 3 stacks
           "mlp_units":  tune.choice([[[512, 512], [512, 512], [512, 512]]]),        # 2 512-Layers per block for each stack
           "interpolation_mode": tune.choice(['linear']),                            # Type of multi-step interpolation
           "val_check_steps": tune.choice([100]),                                    # Compute validation every 100 epochs
           "random_seed": tune.randint(1, 10),
        }
    return nhits_config

def set_nbeats_config(args):

    # Use your own config or AutoNHITS.default_config
    nheats_config = {
           "learning_rate": tune.choice([1e-3]),                                     # Initial Learning rate
           "max_steps": tune.choice([1000]),                                         # Number of SGD steps
           "input_size": tune.choice([args.horizon, args.horizon*2, args.horizon*3, args.horizon*5]),  # input_size = multiplier * horizon
           "batch_size": tune.choice([7]),                                           # Number of series in windows
           "windows_batch_size": tune.choice([256]),                                 # Number of windows in batch
           "activation": tune.choice(['ReLU']),                                      # Type of non-linear activation
           "n_blocks":  tune.choice([[1, 1, 1]]),                                    # Blocks per each 3 stacks
           "mlp_units":  tune.choice([[[512, 512], [512, 512], [512, 512]]]),        # 2 512-Layers per block for each stack
           "val_check_steps": tune.choice([100]),                                    # Compute validation every 100 epochs
           "random_seed": tune.randint(1, 10),
        }
    return nheats_config

def train_model(args):
    models = [
        AutoNHITS(h=args.horizon, config=args.nhits_config, num_samples=args.num_samples),
        AutoNBEATS(h=args.horizon, config=args.nbeats_config, num_samples=args.num_samples),
    ]
    
    nf = NeuralForecast(
        models=models,
        freq=args.freq
    )
    
    if args.cv_use:
        val_size = args.horizon
        test_size = args.horizon
        nf.cross_validation(df=args.data, val_size=val_size,
                            test_size=test_size, n_windows=None)
    else:
        nf.fit(df=args.data)
    
    os.makedirs(args.model_dir, exist_ok=True)
    
    nf.save(path=args.model_dir,
            model_index=None, 
            overwrite=True,
            save_dataset=True)



def check_sagemaker(args):
    ## SageMaker

    if os.environ.get('SM_MODEL_DIR') is not None:
        args.data_dir = os.environ['SM_CHANNEL_TRAINING']
        args.model_dir = os.environ['SM_MODEL_DIR']
    return args


    
def main(args):
    args.data = prepare_dataset(args)
    args.nhits_config = set_nhits_config(args)
    args.nbeats_config = set_nbeats_config(args)
    res = train_model(args)
    
if __name__ == '__main__':
    args = arg_setting()
    args = check_sagemaker(args)
    res = main(args)
