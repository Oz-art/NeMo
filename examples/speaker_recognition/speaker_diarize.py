# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pytorch_lightning import seed_everything

from nemo.collections.asr.models import ClusteringDiarizer
from nemo.core.config import hydra_runner
from nemo.utils import logging

"""
Basic run 
python speaker_diarize.py
"""

seed_everything(42)


@hydra_runner(config_path="conf", config_name="speaker_diarization.yaml")
def main(cfg):

    logging.info(f'Hydra config: {cfg.pretty()}')
    sd_model = ClusteringDiarizer(cfg=cfg)
    sd_model.save_to('/data3/sdtest/models/sd_emb_only.nemo')
    sd_model.restore_from('/data3/sdtest/models/sd_emb_only.nemo')
    vad_config = {
        'model_path': "/data3/sdtest/models/MatchboxNet_VAD_3x2.nemo",
        'window_length_in_sec': 0.63,
        'shift_length_in_sec': 0.01,
        'threshold': 0.5,
        'vad_decision_smoothing': True,
        'smoothing_params': {'method': "median", 'overlap': 0.875},
    }
    sd_model.set_vad_model(vad_config)
    sd_model.diarize()


if __name__ == '__main__':
    main()
