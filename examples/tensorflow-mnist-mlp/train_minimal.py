import tensorflow as tf
import numpy as np
import os

from tensorflow.python.tools import freeze_graph
from tensorflow.python.training import saver as saver_lib
from tensorflow.python.framework import graph_io


epochs = 100
batch_size = 32

work_directory = 'model'
saver_write_version = 2


mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0


def one_hot(x, num_classes):
    y = np.zeros((len(x), num_classes))
    for i in range(len(x)):
        y[i][x[i]] = 1
    return y


y_train_one_hot = one_hot(y_train, 10)
y_test_one_hot = one_hot(y_test, 10)

print(x_train.shape, y_train.shape)

with tf.Session() as sess:

    input = tf.placeholder(tf.float32, shape=(None, 28, 28), name='input')
    flattened = tf.reshape(input, (-1, 28 * 28))

    W1 = tf.Variable(np.random.uniform(0, 1, (28 * 28, 100)), dtype=tf.float32)
    b1 = tf.Variable(np.zeros(100), dtype=tf.float32)
    h1 = tf.matmul(flattened, W1) + b1

    W2 = tf.Variable(np.random.uniform(0, 1, (100, 100)), dtype=tf.float32)
    b2 = tf.Variable(np.zeros(100), dtype=tf.float32)
    h2 = tf.matmul(h1, W2) + b2

    W3 = tf.Variable(np.random.uniform(0, 1, (100, 10)), dtype=tf.float32)
    b3 = tf.Variable(np.zeros(10), dtype=tf.float32)

    prediction = tf.matmul(h2, W3) + b3

    softmax = tf.nn.softmax(prediction, name='output')

    labels = tf.placeholder(tf.float32, (None, 10), name='labels')

    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=prediction))

    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    correct_prediction = tf.equal(
        tf.argmax(prediction, 1), tf.argmax(labels, 1))

    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    checkpoint_prefix = os.path.join(work_directory, "saved_checkpoint")
    checkpoint_meta_graph_file = os.path.join(work_directory,
                                              "saved_checkpoint.meta")
    checkpoint_state_name = "checkpoint_state"
    input_graph_name = "input_graph.pb"
    output_graph_name = "model.pb"

    print("Training model...")

    sess.run(tf.global_variables_initializer())

    for epoch in range(epochs):
        print("Epoch " + str(epoch))
        for i in range(0, len(x_train), batch_size):
            x_batch = x_train[i: i + 32]
            y_batch = y_train_one_hot[i: i + 32]
        train_step.run(feed_dict={input: x_batch, labels: y_batch})

    print("Saving checkpoint...")

    saver = saver_lib.Saver(write_version=saver_write_version)
    checkpoint_path = saver.save(
        sess,
        checkpoint_prefix,
        global_step=0,
        latest_filename=checkpoint_state_name)
    graph_io.write_graph(sess.graph, work_directory, input_graph_name)

    input_graph_path = os.path.join(work_directory, input_graph_name)
    input_saver_def_path = ""
    input_binary = False
    output_node_names = "output"
    restore_op_name = "save/restore_all"
    filename_tensor_name = "save/Const:0"
    output_graph_path = os.path.join(work_directory, output_graph_name)
    clear_devices = False
    input_meta_graph = checkpoint_meta_graph_file

    print("Freezing graph...")

    freeze_graph.freeze_graph(
        input_graph_path,
        input_saver_def_path,
        input_binary,
        checkpoint_path,
        output_node_names,
        restore_op_name,
        filename_tensor_name,
        output_graph_path,
        clear_devices,
        "",
        "",
        input_meta_graph,
        checkpoint_version=saver_write_version)
    print("Graph frozen successfully!")
