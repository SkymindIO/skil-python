import keras
from keras.datasets import mnist
from keras.models import Model
from keras.layers import Dense, Dropout, Input

batch_size = 128
num_classes = 10
epochs = 10

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


inp = Input((784,))
x = Dense(512, activation='relu')(inp)
x = Dropout(0.2)(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.2)(x)
out = Dense(num_classes, activation='softmax')(x)

model = Model(inp, out)

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='sgd', metrics=['accuracy'])


history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))

model.save("model.h5")
