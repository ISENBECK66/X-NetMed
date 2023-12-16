FROM tensorflow/serving:2.7.0

COPY chest_xray-model /models/chest_xray-model/1
ENV MODEL_NAME="chest_xray-model"
