# Timeseries Forecasting on AWS

이 데모는 기존 영문으로 된 [Amazon Forecast workshop](https://github.com/apac-ml-tfc/forecasting-workshop.git) 자료에 부가설명은 한글로 추가하였습니다.

This demo repository walks through an example **time-series forecasting** problem, comparing pre-built timeseries forecasting engine [Amazon Forecast](https://aws.amazon.com/forecast/) with other models trained on data science platform [Amazon SageMaker](https://aws.amazon.com/sagemaker/). We pay particular attention to modern forecasting procedures [DeepAR](https://arxiv.org/abs/1704.04110) and [Prophet](https://peerj.com/preprints/3190.pdf).

The demo is presented as a series of Python notebooks designed to be run in Amazon SageMaker, but with some parts requiring activity in the AWS Console.

## Getting Started

### Setting Up Your Notebook Instance

<table>
<thead>

<tr>
<td align="center">Singapore (ap-southeast-1)</td>
<td align="left"><a  href="https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/create/review?stackName=ForecastDemoLab&amp;templateURL=https://napkin-share.s3.ap-northeast-2.amazonaws.com/cloudformation/amazon-forecast.yml&amp;" target="_blank"  class="btn btn-default">
  <i class="fas fa-play"></i>
Deploy to AWS Singapore
</a>
</td>
</tr>

</tbody>
</table>

First you will need to create a new Notebook Instance, to do that begin by logging into the AWS Console.

Next, ensure you are in a [supported region](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) for Amazon Forecast. We test primarily in `Asia Pacific (Seoul)`.

Under `Find services` in the main body of the page, enter `SageMaker`, then select it from the drop-down.

To the left, will see a category titled `Notebook` inside that, click `Notebook instances`.

Click the orange `Create notebook instance` button.

Give the instance a name unique in the account you are using. If a shared account, place your name first like `FirstNameLastNameForecastDemo`. The default Instance type is fine.

The Next component to change is the IAM role. Under the drop-down click `Create a new role`. Then for S3, select `Any S3 Bucket`, finally click `Create role`.

Note that the role itself has become a link. Open that link in a new tab.

Here you will update the policies of your instance to allow it to work with Forecast. Click the `Attach policies` button.
Search and check the box next to the following policies:
-IAMFullAccess
-AmazonForecastFullAccess

Finally click the `Attach policy` button on the bottom right corner.

Now click on `Trust relationship` tab > click on `Edit trust relationships` button > update the json file with the following:
"Service": [
"forecast.amazonaws.com",
"sagemaker.amazonaws.com"
]

Next click the `Create policy` button at the top. In the new page, click the `JSON` tab.

Erase all of the content that is in the editor and paste the content in [IAM_Policy.json](IAM_Policy.json).

After pasting, click the `Review policy` button. Give the policy again a personalize name like `FirstNameLastNameForecastIAMPolicy`.

For the description, enter in something about it being used to demo Forecast. Finally click `Create policy`. Close this tab or window.

Once closed you should see the tab for adding permissions to your SageMaker role. Click the `Filter Policies` link, then select
`Customer managed`. After that, you should see the policy you just created, if the list is long, just paste the name in the search bar to reduce the number
of items. If you do not see it still, click the refresh icon in the top right of the page.

After clicking the checkbox next to the policy, click `Attach policy` at the bottom of the page. Then close this window.

Back at the SageMaker Notebook Instance creation page, expand out the `Git repositories` section and select to "Clone a public Git repository into this notebook instance only": Provide the URL of this repository.

Now you're ready to click `Create notebook instance` at the bottom of the page. This process will take 5-10 minutes to complete. Once the status says `InService` you are ready to continue.

### Working Through The Notebooks

To begin with your new notebook instance, click `Open Jupyter` or `Open JupyterLab`, this will take you to the default interface for the Notebook Instance.

The `forecastworkshop` folder should already be created for you: Enter it and start by opening Notebook 1.

If prompted for a kernel, select `conda_python3`.

From here you will follow the instructions outlined in the notebook.

**Read every cell FULLY before executing it!**
