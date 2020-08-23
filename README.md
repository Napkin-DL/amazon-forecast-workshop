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


