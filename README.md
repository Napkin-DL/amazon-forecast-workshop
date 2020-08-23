# Timeseries Forecasting on AWS

이 데모는 기존 영문으로 된 [Amazon Forecast workshop](https://github.com/apac-ml-tfc/forecasting-workshop.git) 자료에 부가설명은 한글로 추가하였습니다.

이 데모는 Amazon 예측 서비스인 [Amazon Forecast](https://aws.amazon.com/forecast/)을 AI/ML 플랫폼인 [Amazon SageMaker](https://aws.amazon.com/sagemaker/)에서 데이터 준비 작업을 수행한 다음, Forecast에 적합한 데이터를 이용하여 예측 서비스를 제공하게 됩니다. 이후 Forecast에서 제공되는 [DeepAR] (https://arxiv.org/abs/1704.04110) 및 [Prophet] (https://peerj.com/preprints/3190.pdf)을 이용하여 예측 모델을 생성합니다. 추가적으로, SageMaker에서 사용할 수 있는 DeepAR을 학습한 다음 Forecast에서 학습된 다른 모델과 비교하여 ** 시계열 예측 ** 문제를 해결하는 사례를 보여줍니다. 

데모는 Amazon SageMaker에서 실행되도록 설계된 일련의 Python 노트북으로 제공되지만 실제 Forecast 모델을 생성하는 과정은 AWS 콘솔에서 수행하게 됩니다.

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

먼저 AWS 콘솔에 로그인하여 새 노트북 인스턴스를 생성 합니다.

다음으로 Amazon Forecast의 [supported region] (https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/)에 있는지 확인합니다. 위 CloudFormation으로 생성이 가능하며, Singapore 이외 리전에서 수행하고자 할 경우, 위 CloudFormation을 클릭하여 들어간 다음 AWS console 화면의 오른쪽 상단에서 리전을 변경하면 됩니다. 
CloudFormation이 성공적으로 완성된 다음 AWS '서비스 찾기'에서 'SageMaker'를 입력 한 다음 드롭 다운에서 선택합니다.
왼쪽에 '노트북'이라는 카테고리가 표시되면 '노트북 인스턴스'를 클릭하면, `forecast-demolab-XXX` 이름의 노트북에 대해 `Open Jupyter` or `Open JupyterLab`을 클릭합니다.

노트북은 번호 순서대로 수행하면 되고, 노트북에 수정해야 할 부분이 있기에 이 부분은 **CloudFormation**의 **output**을 참고하여 수정해야 합니다.
