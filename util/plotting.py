# External Dependencies:
from IPython.core.display import display, HTML
import matplotlib as mpl
import matplotlib.pyplot as plt

def plot_fcst_results(actuals, predictions):
    models = predictions["model"].unique()
    customer_types = predictions["customer_type"].unique()
    
    for model in models:
        display(HTML(f"<h3>{model}</h3>"))
        for customer_type in customer_types:
            prediction = predictions[
                (predictions["model"] == model)
                & (predictions["customer_type"] == customer_type)
            ]
            prediction_tsnums = mpl.dates.date2num(prediction["timestamp"])
            actual = actuals[
                actuals["customer_type"] == customer_type
            ]
            
            # Create our figure:
            fig = plt.figure(figsize=(15, 6))
            ax = plt.gca()
            ax.set_title(f"Forecast {customer_type} demand ({model})")

            # A black line plot of the actuals (training + test):
            ax.plot_date(
                mpl.dates.date2num(actual["timestamp"]),
                actual["demand"],
                fmt="-",
                color="black",
                label="Actual"
            )
            # Translucent color-1 fill covering the confidence interval:
            ax.fill_between(
                prediction_tsnums,
                prediction["p10"],
                prediction["p90"],
                alpha=0.3,
                label="80% Confidence Interval"
            )
            # Color-1 line identifying the prediction median:
            ax.plot_date(
                prediction_tsnums,
                prediction["p50"],
                fmt="-",
                label="Prediction Median"
            )
            # Color-2 line identifying the prediction mean:
            ax.plot_date(
                prediction_tsnums,
                prediction["mean"],
                fmt="-",
                label="Prediction Mean"
            )

            ax.set_xlabel("Date")
            ax.set_ylabel("Rides Taken (Demand)")
            ax.legend()
            plt.show()

            
def plot_fcst_merge_results(actuals, predictions):
    models = predictions["model"].unique()
    customer_types = predictions["customer_type"].unique()
    
        
    for customer_type in customer_types:
        display(HTML(f"<h3>{customer_type}</h3>"))
        actual = actuals[
            actuals["customer_type"] == customer_type
        ]
        # Create our figure:
        fig = plt.figure(figsize=(15, 6))
        ax = plt.gca()
        ax.set_title(f"Forecast {customer_type}")

        # A black line plot of the actuals (training + test):
        ax.plot_date(
            mpl.dates.date2num(actual["timestamp"]),
            actual["demand"],
            fmt="-",
            color="black",
            label="Actual"
        )
        
        for model in models:
            prediction = predictions[
                (predictions["model"] == model)
                & (predictions["customer_type"] == customer_type)
            ]
            prediction_tsnums = mpl.dates.date2num(prediction["timestamp"])
            

            # Translucent color-1 fill covering the confidence interval:
            ax.fill_between(
                prediction_tsnums,
                prediction["p10"],
                prediction["p90"],
                alpha=0.3,
                label=f"80% Confidence Interval for {model}"
            )
            # Color-1 line identifying the prediction median:
            ax.plot_date(
                prediction_tsnums,
                prediction["p50"],
                fmt="-",
                label=f"Prediction Median for {model}"
            )
            # Color-2 line identifying the prediction mean:
            ax.plot_date(
                prediction_tsnums,
                prediction["mean"],
                fmt="-",
                label=f"Prediction Mean for {model}"
            )

        ax.set_xlabel("Date")
        ax.set_ylabel("Rides Taken (Demand)")
        ax.legend()
        plt.show()