import os
import uuid
import keras


class PickleableKerasModelWrapper(object):
    def __init__(self, model):
        self.model = model


    def __getattr__(self, model_attribute_name):
        return getattr(self.model, model_attribute_name)


    def __getstate__(self):
        state = self.__dict__.copy()

        # code to save model & weights
        model_json = self.model.to_json()
        h5_filename = "{}.model.h5".format(uuid.uuid1())
        self.model.save_weights(h5_filename)
        with open(h5_filename, "rb") as f:
            weights_h5_binary = f.read()
        os.remove(h5_filename)

        state.update({"model": {"json": model_json, "weights": weights_h5_binary}})
        return state


    def __setstate__(self, state):
        model_json = state["model"]["json"]
        weights_h5_binary = state["model"]["weights"]

        # code to load model & weights
        model = keras.models.model_from_json(model_json)
        h5_filename = "{}.model.h5".format(uuid.uuid1())
        with open(h5_filename, "wb") as f:
            f.write(weights_h5_binary)
        model.load_weights(h5_filename)
        os.remove(h5_filename)

        state.update({"model": model})
        self.__dict__.update(state)
