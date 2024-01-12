from keras.layers import Dense
from keras.models import Sequential
from tensorflow import keras
from training.ann_base import AnnBase


class AnnRegression(AnnBase):

    def get_model(self):
        model = Sequential()
        if self.number_of_hidden_layers > 0:
           model.add(Dense(self._number_of_neurons_in_first_hidden_layer, input_shape=(1, self.__number_of_train_columns), kernel_initializer=self.kernel_initializer, activation=self.activation_function))
           if self.number_of_hidden_layers > 1:
               for i in range(self.number_of_hidden_layers - 1):
                   model.add(Dense(self.number_of_neurons_in_other_hidden_layers, kernel_initializer=self.kernel_initializer, activation=self.activation_function))
        model.add(Dense(1, kernel_initializer=self.kernel_initializer))        
        return model

    def use_model_from_path(self):
        self.model = keras.models.load_model(self.__modelName)

    def compile_and_fit(self, trainX, trainY):
        self.model = self.get_model()
        self.model.compile(loss=self.cost_function, optimizer=self.optimizer)
        self.trainX = trainX
        self.model.fit(trainX, trainY, epochs=self.epoch_number, batch_size=self.batch_size_number, verbose=self.verbose)
        self.model.save(self.__modelName)

    def get_test_predict(self, testX):
        return self.model.predict(testX)
    
    def get_train_predict(self, testX):
        trainPredict = self.model.predict(self.trainX)
        testPredict = self.model.predict(testX)
        return trainPredict, testPredict

    def compile_fit_predict(self, trainX, trainY, testX):
        self.compile_and_fit(trainX, trainY)
        return self.get_train_predict(testX)

    def set_model_name(self, modelName):
        self.__modelName = f"models/{modelName}"

    def set_number_of_train_columns(self, number_of_train_columns):
        self.__number_of_train_columns = number_of_train_columns

