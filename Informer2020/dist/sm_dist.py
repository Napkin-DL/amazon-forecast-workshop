########################################################
####### 1. SageMaker Distributed Data Parallel  ########
#######  - Import Package and Initialization    ########
########################################################
import torch

try:
    import smdistributed.dataparallel.torch.torch_smddp
except:
    print("NO SageMaker DDP")
    pass
    
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

import os
#######################################################


def dist_set(args):
    if args.use_multi_gpu:
        backend = 'smddp'
    else:
        backend = 'nccl'
        
    dist.init_process_group(backend=backend)
    args.rank = dist.get_rank()
    args.local_rank = args.rank%int(os.environ['SM_NUM_GPUS'])
    args.world_size = dist.get_world_size()
    
    os.environ['LOCAL_RANK'] = str(args.local_rank)

    if torch.cuda.is_available():
        torch.cuda.set_device(args.local_rank)
    
    args.batch_size //= args.world_size
    args.batch_size = max(args.batch_size, 1)
    return args


def dist_model(model):
    local_rank = int(os.environ['LOCAL_RANK'])
    model = DDP(model, 
                broadcast_buffers=False,
                device_ids=[local_rank],
                output_device=local_rank
               )
    return model
    

def barrier():
    return dist.barrier()