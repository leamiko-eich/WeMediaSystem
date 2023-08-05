#encoding=utf-8

import enum

class RecallFlowStep(enum.Enum):
    Step0_init_line = "0_init_line"
    Step1_add_totask = "1_addto_task"

    
    
if __name__=="__main__":
    obj = RecallFlowStep.Step0_init_line.value
    print(type(obj))
    print(obj)