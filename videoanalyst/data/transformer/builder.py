# -*- coding: utf-8 -*-

from typing import Dict, List

from yacs.config import CfgNode

from .transformer_base import TASK_TRANSFORMERS, TransformerBase
from videoanalyst.utils import merge_cfg_into_hps


def build(task: str, cfg: CfgNode, seed: int=0) -> TransformerBase:
    r"""
    Arguments
    ---------
    task: str
        task
    cfg: CfgNode
        node name: transformer
    """
    assert task in TASK_TRANSFORMERS, "invalid task name"
    MODULES = TASK_TRANSFORMERS[task]

    names = cfg.names
    modules = []

    for name in names:
        module = MODULES[name](seed=seed)
        hps = module.get_hps()
        hps = merge_cfg_into_hps(cfg[name], hps)
        module.set_hps(hps)
        module.update_params()

        modules.append(module)

    return modules


def get_config() -> Dict[str, CfgNode]:
    cfg_dict = {name: CfgNode() for name in task_datasets.keys()}

    for cfg_name, modules in task_datasets.items():
        cfg = cfg_dict[cfg_name]
        cfg["names"] = []

        for name in modules:
            cfg[name] = CfgNode()
            module = modules[name]
            hps = module.default_hyper_params
            for hp_name in hps:
                cfg[name][hp_name] = hps[hp_name]

    return cfg_dict
