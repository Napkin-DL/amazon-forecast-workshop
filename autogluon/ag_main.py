import os
import argparse
import pandas as pd
from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor


def arg_setting():
    parser = argparse.ArgumentParser(description='[Informer] Long Sequences Forecasting')

    parser.add_argument('--prediction_length', type=int, default=336, help='forecasting horizon')
    parser.add_argument('--data_dir', type=str, default='./data/amzforecast/', help='data file')
    parser.add_argument('--model_dir', type=str, default='./model', help='store result')
    args = parser.parse_args()
    return args


def prepare_dataset(args):
    train_df = pd.read_csv(f'{args.data_dir}/target_train.csv')
    related_df = pd.read_csv(f'{args.data_dir}/related.csv')
    
    # data_df = pd.concat([train_df,test_df])
    data_df = train_df
    data = pd.merge(data_df, related_df, on=['timestamp', 'item_id'], how='left')
    data = data.sort_values(by=['item_id', 'timestamp']).reset_index(drop=True)

    
    train_data = TimeSeriesDataFrame.from_data_frame(
        data,
        id_column="item_id",
        timestamp_column="timestamp"
    )
    return train_data

def train_model(args):
    predictor = TimeSeriesPredictor(
        prediction_length=args.prediction_length,
        path=args.model_dir,
        target="demand",
        eval_metric="sMAPE"
    )

    predictor.fit(
        args.data,
        presets="medium_quality",
        time_limit=600,
    )



def check_sagemaker(args):
    ## SageMaker

    if os.environ.get('SM_MODEL_DIR') is not None:
        args.data_dir = os.environ['SM_CHANNEL_TRAINING']
        args.model_dir = os.environ['SM_MODEL_DIR']
    return args


def main(args):
    args.data = prepare_dataset(args)
    res = train_model(args)


if __name__ == '__main__':
    args = arg_setting()
    args = check_sagemaker(args)
    res = main(args)
