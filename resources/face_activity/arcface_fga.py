from __future__ import division
import mxnet as mx
import numpy as np
import cv2

class FaceGenderage:
    def __init__(self, param_file):
        self.param_file = param_file
        self.image_size = (112, 112)

    def prepare(self, ctx_id):
        if self.param_file:
            prefix = self.param_file['prefix']
            epoch = self.param_file['epoch']
            sym, arg_params, aux_params = mx.model.load_checkpoint(prefix, epoch)
            all_layers = sym.get_internals()
            sym = all_layers['fc1_output']
            if ctx_id>=0:
                ctx = mx.gpu(ctx_id)
            else:
                ctx = mx.cpu()
            model = mx.mod.Module(symbol=sym, context=ctx, label_names = None)
            data_shape = (1,3)+self.image_size
            model.bind(data_shapes=[('data', data_shape)])
            model.set_params(arg_params, aux_params)
            #warmup
            data = mx.nd.zeros(shape=data_shape)
            db = mx.io.DataBatch(data=(data,))
            model.forward(db, is_train=False)
            embedding = model.get_outputs()[0].asnumpy()
            self.model = model
        else:
            pass

    def get(self, img):
        data = cv2.resize(img, self.image_size)
        data = np.transpose(data, (2,0,1))
        data = np.expand_dims(data, axis=0)
        data = mx.nd.array(data)
        db = mx.io.DataBatch(data=(data,))
        self.model.forward(db, is_train=False)
        ret = self.model.get_outputs()[0].asnumpy()
        g = ret[:,0:2].flatten()
        gender = np.argmax(g)
        a = ret[:,2:202].reshape( (100,2) )
        a = np.argmax(a, axis=1)
        age = int(sum(a))
        return gender, age