import sys
import multiprocessing as mp
import numpy as np
import torch
import torch.utils.data


class NeuralNetwork(object):
    def __init__(self,
                 model,
                 loss_function_class,
                 optimizer_class,

                 loss_function_params={},
                 optimizer_params={'lr': 0.1},

                 n_epochs=200,
                 batch_size=64,

                 n_jobs=-1,
                 log=sys.stdout,
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


    def __log_loss(self, epoch_idx, batch_idx, loss):
        self.log.write(
            "[epoch {}/{}, batch {}/{}]: loss: {}\n".format(
                epoch_idx, self.n_epochs,
                batch_idx, int(self._n_samples/self.batch_size),
                loss))


    def __batch(self, batch_X, batch_y):
        batch_X, batch_y = self.__to_variable(batch_X), self.__to_variable(batch_y)

        y_pred = self.model(batch_X)

        loss = self.loss(y_pred, batch_y)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.data[0]


    def __epoch(self, epoch_idx):
        for batch_idx, (batch_X, batch_y) in enumerate(self._data_loader):
            loss = self.__batch(batch_X, batch_y)
            self.__log_loss(epoch_idx, batch_idx, loss)


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