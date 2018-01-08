import sys
import multiprocessing as mp
import numpy as np
import torch
import torch.utils.data
from ..experiment import Dataset
from .operators import unwrapped
from .learner import LearnerWrapper, Event
from .onehot import OneHotClassifierWrapper
from ..utils.conversion import collect_classes, per_sample_shape, labels_to_one_hots
from ..utils.arguments import null_function
from ..utils.writer import StdOutOutput
from time import sleep
import math


class AbstractNeuralNetwork(object):
    def __init__(self,
                 model,
                 loss_function_class,
                 optimizer_class,

                 loss_function_params={},
                 optimizer_params={'lr': 0.1},

                 n_epochs=200,
                 batch_size=64,

                 n_jobs=-1,
                 log=StdOutOutput(),
                 use_gpu=True):

        self.model = model
        self.loss = loss_function_class(**loss_function_params)
        self.optimizer = optimizer_class(self.model.parameters(), **optimizer_params)

        self.n_epochs = n_epochs
        self.batch_size = batch_size

        self.workers = n_jobs if n_jobs > 0 else mp.cpu_count()
        self.log = log
        self.use_gpu = use_gpu

        self._n_samples = 0
        self._data_loader = None

        if self.use_gpu:
            self.model = self.model.cuda()

        self.validation_dataset = None
        self.test_dataset = None


    def __to_variable(self, tensor):
        variable = torch.autograd.Variable(tensor)
        if self.use_gpu:
            return variable.cuda()
        return variable


    def __to_numpy(self, variable):
        data = variable.data
        if 'cuda' in data.__class__.__module__:
            return data.cpu().numpy()
        return data.numpy()


    def __log(self, epoch_idx, batch_idx, loss, validation_loss=None, test_loss=None):
        self.log.write(r'{',
                       '"epoch": {}, "n_epochs": {}, "batch": {}, "n_batches": {}, "training loss": {}{}{}'.format(
                           epoch_idx,
                           self.n_epochs,
                           batch_idx,
                           int(self._n_samples/self.batch_size),
                           loss,
                           ', "validation loss": {}'.format(validation_loss) if validation_loss is not None else "",
                           ', "test loss": {}'.format(test_loss) if test_loss is not None else ""),
                       r'}', '\n')


    def __batch(self, batch_X, batch_y):
        batch_X, batch_y = self.__to_variable(batch_X), self.__to_variable(batch_y)

        y_pred = self.model(batch_X)

        loss = self.loss(y_pred, batch_y)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.data[0]


    def __validation_loss(self):
        if not self.validation_dataset:
            return None

        valid_pred = self.model(self.validation_dataset["X"])
        loss = self.loss(valid_pred, self.validation_dataset["y"])
        return loss.data[0]


    def __test_loss(self):
        if not self.test_dataset:
            return None

        test_pred = self.model(self.test_dataset["X"])
        loss = self.loss(test_pred, self.test_dataset["y"])
        return loss.data[0]


    def __epoch(self, epoch_idx):
        for batch_idx, (batch_X, batch_y) in enumerate(self._data_loader):
            loss = self.__batch(batch_X, batch_y)

            validation_loss = None
            test_loss = None
            if (epoch_idx % (math.ceil(self.n_epochs * 0.05)) == 0) and batch_idx == 0:
                validation_loss = self.__validation_loss()
                test_loss = self.__test_loss()

            self.__log(epoch_idx, batch_idx, loss, validation_loss, test_loss)


    def register_validation_dataset(self, validation_dataset):
        self.validation_dataset = {
            "X": self.__to_variable(torch.from_numpy(validation_dataset.X)),
            "y": self.__to_variable(torch.from_numpy(validation_dataset.y))
        }


    def register_test_dataset(self, validation_dataset):
        self.test_dataset = {
            "X": self.__to_variable(torch.from_numpy(validation_dataset.X)),
            "y": self.__to_variable(torch.from_numpy(validation_dataset.y))
        }


    def __getstate__(self):
        state = {key: value for key, value in self.__dict__.items() if key not in ["validation_dataset", "test_dataset"]}
        return state


    def __setstate__(self, state):
        self.__dict__.update(state)


    def fit(self, X, y):
        X = torch.from_numpy(np.array(X))
        y = torch.from_numpy(np.array(y))

        dataset = torch.utils.data.TensorDataset(X, y)
        self._n_samples = len(dataset)

        self._data_loader = torch.utils.data.DataLoader(
            dataset, batch_size=self.batch_size, shuffle=True,
            num_workers=self.workers, pin_memory=True, sampler=None)

        for epoch_idx in range(self.n_epochs):
            self.__epoch(epoch_idx)


    def predict(self, X):
        X = torch.from_numpy(np.array(X))

        pred = self.model(self.__to_variable(X))

        return self.__to_numpy(pred)


class SeedInitializerMixin(object):
    def __init__(self, seed=None):
        self.seed = seed

        self.init_seed()


    def init_seed(self):
        if self.seed is not None:
            print("setting torch seed")
            torch.manual_seed(self.seed)


class AbstractOneHotNeuralNetwork(SeedInitializerMixin):
    def __init__(self, *args, y_dtype=None, seed=None, **kwargs):
        SeedInitializerMixin.__init__(self, seed)

        self.learner = OneHotClassifierWrapper(AbstractNeuralNetwork, *args, y_dtype=y_dtype, **kwargs)
        self.validation_dataset = None
        self.y_dtype = y_dtype


    def get_model(self, input_dim, output_dim):
        raise RuntimeError("no get_model method overridden")


    def register_evaluation_datasets(self, validation_dataset, test_dataset=None):
        def convert_to_onehot(emitter, validation_dataset, test_dataset=None):
            unwrapped(self.learner).learner.register_validation_dataset(Dataset(
                validation_dataset.X,
                labels_to_one_hots(validation_dataset.y, self.learner.get_classes(), dtype=self.y_dtype)
            ))
            if test_dataset is not None:
                unwrapped(self.learner).learner.register_test_dataset(Dataset(
                    test_dataset.X,
                    labels_to_one_hots(test_dataset.y, self.learner.get_classes(), dtype=self.y_dtype)
                ))

        self.learner.register_event("classes_collected", Event(convert_to_onehot, validation_dataset, test_dataset))


    def fit(self, X, y):
        self.learner.instantiate_estimator(model=self.get_model(per_sample_shape(X), len(collect_classes(y))))
        return self.learner.fit(X, y)


    def predict(self, X):
        return self.learner.predict(X)
