# import pandas as pd
import numpy as np
import tensorflow as tf
import tkinter as tk
from collections import Counter
from sklearn.datasets import fetch_20newsgroups
numbers = 9
vocab = Counter()



def get_word_2_index(vocab):
    word2index = {}
    for i, word in enumerate(vocab):
        word2index[word] = i
    return word2index
root = tk.Tk()
root.title('Neural network for text classification')
root.geometry('650x450+300+200')
root.resizable(False, False)
Title = tk.Label(text="Welcome", width = 600, font = 'Arial 14 bold', bg='#54ff9f')
Title.pack()
# print("Hi:", matrix)
root.update()
categories = ['comp.graphics','comp.os.ms-windows.misc','comp.sys.ibm.pc.hardware','comp.sys.mac.hardware','comp.windows.x','sci.crypt','sci.electronics','sci.med','sci.space',]
newsgroups_train = fetch_20newsgroups(subset='train', categories=categories)
newsgroups_test = fetch_20newsgroups(subset='test', categories=categories)

print('total texts in train:', len(newsgroups_train.data))
print('total texts in test:', len(newsgroups_test.data), '\n')


vocab = Counter()

for text in newsgroups_train.data:
    for word in text.split(' '):
        vocab[word.lower()] += 1

for text in newsgroups_test.data:
    for word in text.split(' '):
        vocab[word.lower()] += 1

print("Total words:", len(vocab))

total_words = len(vocab)


def get_word_2_index(vocab):
    word2index = {}
    for i, word in enumerate(vocab):
        word2index[word.lower()] = i

    return word2index


word2index = get_word_2_index(vocab)



def text_to_vector(text):
    layer = np.zeros(total_words, dtype=float)
    for word in text.split(' '):
        layer[word2index[word.lower()]] += 1

    return layer


def category_to_vector(category):
    y = np.zeros(10, dtype=float)
    if category == 0:
        y[0] = 1.
    elif category == 1:
        y[1] = 1.
    elif category == 2:
        y[2] = 1.
    elif category == 3:
        y[3] = 1.
    elif category == 4:
        y[4] = 1.
    elif category == 5:
        y[5] = 1.
    elif category == 6:
        y[6] = 1.
    elif category == 7:
        y[7] = 1.
    elif category == 8:
        y[8] = 1.
    else:
        y[9] = 1.


    return y


def get_batch(df, i, batch_size):
    batches = []
    results = []
    texts = df.data[i * batch_size:i * batch_size + batch_size]
    categories = df.target[i * batch_size:i * batch_size + batch_size]

    for text in texts:
        layer = text_to_vector(text)
        batches.append(layer)

    for category in categories:
        y = category_to_vector(category)
        results.append(y)

    return np.array(batches), np.array(results)



# Parameters
learning_rate = 0.05
training_epochs = 8
batch_size = 150
display_step = 1

# Network Parameters
n_hidden_1 = 300       # 1st layer number of features
n_hidden_2 = 300      # 2nd layer number of features
# n_hidden_3 = 300       # 3th layer number of features
# n_hidden_4 = 300       # 4rd layer number of features
n_input = total_words  # Words in vocab
n_classes = 10         # Categories

input_tensor = tf.placeholder(tf.float32, [None, n_input], name="input")
output_tensor = tf.placeholder(tf.float32, [None, n_classes], name="output")


def multilayer_perceptron(input_tensor, weights, biases):
    layer_1_multiplication = tf.matmul(input_tensor, weights['h1'])
    layer_1_addition = tf.add(layer_1_multiplication, biases['b1'])
    layer_1 = tf.nn.relu(layer_1_addition)

    # Hidden layer with RELU activation
    layer_2_multiplication = tf.matmul(layer_1, weights['h2'])
    layer_2_addition = tf.add(layer_2_multiplication, biases['b2'])
    layer_2 = tf.nn.relu(layer_2_addition)
    #
    # # Hidden layer with RELU activation
    # layer_3_multiplication = tf.matmul(layer_2, weights['h3'])
    # layer_3_addition = tf.add(layer_3_multiplication, biases['b3'])
    # layer_3 = tf.nn.relu(layer_3_addition)
    #
    # # Hidden layer with RELU activation
    # layer_4_multiplication = tf.matmul(layer_3, weights['h4'])
    # layer_4_addition = tf.add(layer_4_multiplication, biases['b4'])
    # layer_4 = tf.nn.relu(layer_4_addition)

    # Output layer
    out_layer_multiplication = tf.matmul(layer_2, weights['out'])
    out_layer_addition = out_layer_multiplication + biases['out']

    return out_layer_addition


# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    # 'h3': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3])),
    # 'h4': tf.Variable(tf.random_normal([n_hidden_3, n_hidden_4])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    # 'b3': tf.Variable(tf.random_normal([n_hidden_3])),
    # 'b4': tf.Variable(tf.random_normal([n_hidden_4])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Construct model
prediction = multilayer_perceptron(input_tensor, weights, biases)

# Define loss and optimizer
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=output_tensor))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

# Initializing the variables
init = tf.global_variables_initializer()

# [NEW] Add ops to save and restore all the variables
saver = tf.train.Saver()
# Launch the graph
def startTrain():
    with tf.Session() as sess:
        sess.run(init)
        # Training cycle
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(len(newsgroups_train.data) / batch_size)
            # Loop over all batches
            for i in range(total_batch):
                batch_x, batch_y = get_batch(newsgroups_train, i, batch_size)
                # Run optimization op (backprop) and cost op (to get loss value)
                c, _ = sess.run([loss, optimizer], feed_dict={input_tensor: batch_x, output_tensor: batch_y})
                # Compute average loss
                avg_cost += c / total_batch
            # Display logs per epoch step
            if epoch % display_step == 0:
                EpochLabelText = "Epoch:" + '%04d' % (epoch + 1) + "loss=" + "{:.9f}".format(avg_cost)
                EpochLabel = tk.Label(bg='white', fg='black', width=100, text = EpochLabelText, font='Ariel 10')
                print("Epoch:", '%04d' % (epoch + 1), "loss=",
                      "{:.9f}".format(avg_cost))
                EpochLabel.pack()

        print("Optimization Finished!")

        # Test model
        correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(output_tensor, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        total_test_data = len(newsgroups_test.target)
        batch_x_test, batch_y_test = get_batch(newsgroups_test, 0, total_test_data)
        print("Accuracy:", accuracy.eval({input_tensor: batch_x_test, output_tensor: batch_y_test}))
        predictLabelText = "Accuracy:" + str(accuracy.eval({input_tensor: batch_x_test, output_tensor: batch_y_test}))
        predictLabel = tk.Label(bg='white', fg='black', width=100, text = predictLabelText, font='Arial 10')
        predictLabel.pack()
        analiseButton.config(command = "Null")
        root.update()
        # [NEW] Save the variables to disk
        save_path = saver.save(sess, "/tmp/model.ckpt")

    # Get a text to make a prediction
analiseButton = tk.Button(command = startTrain, text = "Launch Training", width = 100, font = 'Arial 14 bold', activebackground ='#54ff9f', bg='#00FFFF')
analiseButton.pack()
def MakePredict(textForPredict):
    text_for_prediction = textForPredict
    layer = np.zeros(total_words, dtype=float)
    for word in text_for_prediction.split(' '):
        if word.lower() in vocab:
            layer[word2index[word.lower()]] += 1

    vector_txt = layer

    input_array = np.array([vector_txt])

    input_array.shape
    saver = tf.train.Saver()

    with tf.Session() as sess:
        saver.restore(sess, "/tmp/model.ckpt")

        classification = sess.run(tf.argmax(prediction, 1), feed_dict={input_tensor: input_array})
        return categories[int(classification)]


def getEntryAndMakePredict():
    textForPredict = textEntry.get()
    predictLabel.config(text = str(MakePredict(textForPredict)))
textEntry = tk.Entry(width=100)
b = tk.Button(width=100, command=getEntryAndMakePredict, text = "Make predict for text", activebackground= '#54ff9f', font = 'Arial 14 bold', bg='#00FFFF')
predictLabel = tk.Label(bg='#54ff9f', fg='black', width=200, height=1, text='', font='Arial 10')


textEntry.pack()
b.pack()
predictLabel.pack()

root.mainloop()