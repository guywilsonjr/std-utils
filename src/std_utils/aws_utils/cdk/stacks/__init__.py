from inspect import ismodule

import aws_cdk


#print({k: v for k, v in pipelines.__dict__.items() if isclass(v)})
#print({k: v for k, v in aws_cdk.__dict__.items() if not ismodule(v)})
print(aws_cdk.__dict__)
